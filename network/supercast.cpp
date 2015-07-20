#include "supercast.h"

Supercast* Supercast::singleton = NULL;
Supercast* Supercast::getInstance() {return Supercast::singleton;}

Supercast::Supercast(QObject* parent) : QObject(parent)
{
    this->user_name = "";
    this->user_pass = "";
    this->data_base_url = QUrl();

    Supercast::singleton = this;
    this->channels = new QHash<QString, SupercastSignal*>();
    this->queries       = new QHash<int, SupercastSignal*>();
    this->http_requests = new QHash<int, SupercastSignal*>();

    SupercastSignal* sig = new SupercastSignal();
    this->channels->insert("supercast", sig);
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleSupercastMessage(QJsonObject)));

    /*
     * init SupercastHTTP
     */
    SupercastHTTP* http_t = new SupercastHTTP();
    qRegisterMetaType<SupercastHttpReply>("SupercastHttpReply");
    QObject::connect(
                http_t, SIGNAL(serverReply(SupercastHttpReply)),
                this,   SLOT(handleHttpReply(SupercastHttpReply)),
                Qt::QueuedConnection);
    qRegisterMetaType<SupercastHttpRequest>("SupercastHttpRequest");
    QObject::connect(
                this,   SIGNAL(clientHttpRequest(SupercastHttpRequest)),
                http_t, SLOT(handleClientRequest(SupercastHttpRequest)),
                Qt::QueuedConnection);
    http_t->moveToThread(&this->http_thread);
    QObject::connect(
                &this->http_thread, SIGNAL(finished()),
                http_t,               SLOT(deleteLater()));
    this->http_thread.start();
}


void Supercast::tryConnect(
        QHostAddress host,
        qint16       port,
        QString      user_name,
        QString      user_pass)
{
    this->user_name = user_name;
    this->user_pass = user_pass;
    this->data_base_url.setHost(host.toString());

    SupercastSocket* socket_t = new SupercastSocket(host,port);

    // server -> message -> client
    QObject::connect(
                socket_t, SIGNAL(serverMessage(QJsonObject)),
                this,     SLOT(routeServerMessage(QJsonObject)),
                Qt::QueuedConnection);
    // client -> message -> server
    QObject::connect(
                this,     SIGNAL(clientMessage(QJsonObject)),
                socket_t, SLOT(handleClientMessage(QJsonObject)),
                Qt::QueuedConnection);

    // socket state
    qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                socket_t->socket,
                    SIGNAL(error(QAbstractSocket::SocketError)),
                this,
                    SLOT(socketError(QAbstractSocket::SocketError)),
                Qt::QueuedConnection);
    QObject::connect(
                socket_t->socket, SIGNAL(connected()),
                this,             SLOT(socketConnected()),
                Qt::QueuedConnection);

    socket_t->moveToThread(&this->socket_thread);
    QObject::connect(
                &this->socket_thread, SIGNAL(finished()),
                socket_t,             SLOT(deleteLater()));
    this->socket_thread.start();
}


Supercast::~Supercast()
{
    this->http_thread.quit();
    this->socket_thread.quit();

    this->http_thread.wait();
    this->socket_thread.wait();

    delete this->channels;
    delete this->queries;
    delete this->http_requests;
}


/*
 * SLOTS
 */
void Supercast::socketConnected()
{
    QJsonObject authResp {
        {"from", "supercast"},
        {"type", "authResp"},
        {"value", QJsonObject {
            {"name",     this->user_name},
            {"password", this->user_pass}}}};

    emit this->clientMessage(authResp);
}


void Supercast::socketError(QAbstractSocket::SocketError error)
{
    emit this->connectionStatus(error);
}


void Supercast::routeServerMessage(QJsonObject msg)
{

    /*
     * Test if message is for a channel.
     */
    QString from = msg.value("from").toString("undefined");
    if (this->channels->contains(from)) {
        SupercastSignal* sig = this->channels->value(from);
        emit sig->serverMessage(msg);
        return;
    }


    QString msg_type = msg.value("type").toString("undefined");
    /*
     * Then it must be a reply message or subscribe reply
     */
    if(msg_type == "reply") {

        int  queryId = msg.take("queryId").toInt(QUERYID_UNDEF);
        bool lastPdu = msg.take("lastPdu").toBool(true);
        if (queryId == QUERYID_UNDEF) return;

        SupercastSignal* sig = this->queries->value(queryId);
        emit sig->serverMessage(msg);

        if (lastPdu) {
            this->queries->remove(queryId);
            sig->deleteLater();
        }

        return;
    }

    qDebug() << "unknown msg type: " << msg;
}


void Supercast::handleSupercastMessage(QJsonObject message)
{
    QString type = message.value("type").toString("undefined");
    if (type == "authAck") {
        emit this->connectionStatus(Supercast::ConnectionSuccess);
    } else if (type == "authErr") {
        emit this->connectionStatus(Supercast::AuthenticationError);
    } else if (type == "serverInfo") {
        QJsonObject val = message.value("value").toObject();
        this->data_base_url.setPort(val.value("dataPort").toInt());
        this->data_base_url.setScheme(val.value("dataProto").toString());
    } else if (type == "subscribeOk" || type == "subscribeErr") {
        QString channel = message.value("value").toObject().value("channel").toString();
        SupercastSignal* sig = this->channels->value(channel);
        emit sig->serverMessage(message);
    } else if (type == "unsubscribeOk" || type == "unsubscribeErr") {
        qDebug() << "unsubseribe what? " << type;
        return;
    } else {
        qDebug() << "should handle this message?";
    }
}

void Supercast::subscribe(QString channel, SupercastSignal* subscriber)
{
    QJsonObject subscribeMsg {
        {"from", "supercast"},
        {"type", "subscribe"},
        {"value", QJsonObject {
                {"queryId", 0},
                {"channel", channel}}}};
    Supercast::singleton->channels->insert(channel, subscriber);
    emit Supercast::singleton->clientMessage(subscribeMsg);
}

void Supercast::unsubscribe(QString channel)
{
    QJsonObject unsubscribeMsg {
        {"from", "supercast"},
        {"type", "unsubscribe"},
        {"value", QJsonObject {
                {"queryId", 0},
                {"channel", channel}}}};
    Supercast::singleton->channels->remove(channel);
    emit Supercast::singleton->clientMessage(unsubscribeMsg);
}

void Supercast::sendQuery(QJsonObject query, SupercastSignal *reply)
{
    int queryId = 0;
    while (Supercast::singleton->queries->contains(queryId)) queryId += 1;

    Supercast::singleton->queries->insert(queryId, reply);
    query.insert("queryId", queryId);
    emit Supercast::singleton->clientMessage(query);
}

void Supercast::httpGet(QString path, SupercastSignal *reply)
{
    int queryId = 0;
    QUrl url(Supercast::singleton->data_base_url);
    url.setPath(path);
    while (Supercast::singleton->http_requests->contains(queryId)) queryId += 1;
    Supercast::singleton->http_requests->insert(queryId, reply);
    emit Supercast::singleton->clientHttpRequest(SupercastHttpRequest(queryId, url));
}

void Supercast::httpGet(QString path, QString dst_file, SupercastSignal *reply)
{
    int queryId = 0;
    QUrl url(Supercast::singleton->data_base_url);
    url.setPath(path);
    while (Supercast::singleton->http_requests->contains(queryId)) queryId += 1;
    Supercast::singleton->http_requests->insert(queryId, reply);
    emit Supercast::singleton->clientHttpRequest(SupercastHttpRequest(queryId, dst_file, url));

}

void Supercast::httpGet(
        QString          path,
        QString          dst_file,
        SupercastSignal* reply,
        QString          opaque)
{
    int queryId = 0;
    QUrl url(Supercast::singleton->data_base_url);
    url.setPath(path);
    while (Supercast::singleton->http_requests->contains(queryId)) queryId += 1;
    Supercast::singleton->http_requests->insert(queryId, reply);
    SupercastHttpRequest request(queryId, dst_file, url, opaque);
    emit Supercast::singleton->clientHttpRequest(request);

}

void Supercast::handleHttpReply(SupercastHttpReply reply)
{
    int queryId = reply.id;
    SupercastSignal* sig = Supercast::singleton->http_requests->take(queryId);
    emit sig->serverMessage(reply.body);
    sig->deleteLater();
}
