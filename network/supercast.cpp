#include "supercast.h"

Supercast* Supercast::singleton = NULL;
Supercast* Supercast::getInstance() {return Supercast::singleton;}

Supercast::Supercast(QObject* parent) : QObject(parent)
{
    Supercast::singleton = this;
    SupercastSignal* sig = new SupercastSignal(this);
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleSupercastMessage(QJsonObject)));

    this->message_processors = new QHash<QString, SupercastSignal*>();
    this->message_processors->insert("supercast", sig);
    this->queries = new QMap<int, SupercastSignal*>();
}


void Supercast::tryConnect(
        QHostAddress host,
        qint16       port,
        QString      user_name,
        QString      user_pass)
{
    this->user_name = user_name;
    this->user_pass = user_pass;
    SupercastSocket* socket_sup = new SupercastSocket(host,port);

    // server -> message -> client
    QObject::connect(
                socket_sup, SIGNAL(serverMessage(QJsonObject)),
                this,       SLOT(routeServerMessage(QJsonObject)),
                Qt::QueuedConnection);
    // client -> message -> server
    QObject::connect(
                this,       SIGNAL(clientMessage(QJsonObject)),
                socket_sup, SLOT(handleClientMessage(QJsonObject)),
                Qt::QueuedConnection);

    // socket state
    qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                socket_sup->socket,
                    SIGNAL(error(QAbstractSocket::SocketError)),
                this,
                    SLOT(socketError(QAbstractSocket::SocketError)),
                Qt::QueuedConnection);
    QObject::connect(
                socket_sup->socket, SIGNAL(connected()),
                this,               SLOT(socketConnected()),
                Qt::QueuedConnection);

    socket_sup->moveToThread(&this->socket_thread);
    QObject::connect(
                &this->socket_thread, SIGNAL(finished()),
                socket_sup,           SLOT(deleteLater()));
    this->socket_thread.start();
}


Supercast::~Supercast()
{
    this->socket_thread.quit();
    this->socket_thread.wait();
    delete this->message_processors;
    delete this->queries;
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
            {"name",        this->user_name},
            {"password",    this->user_pass}}}};

    emit this->clientMessage(authResp);
}


void Supercast::socketError(QAbstractSocket::SocketError error)
{
    emit this->connexionStatus(error);
}


void Supercast::routeServerMessage(QJsonObject msg)
{

    /*
     * Test if message is for message_processor.
     * TODO "subscribe" to channel should be enought?
     */
    QString from = msg.value("from").toString("undefined");
    if (this->message_processors->contains(from)) {
        SupercastSignal* sig = this->message_processors->value(from);
        emit sig->serverMessage(msg);
        return;
    }


    /*
     * Then it must be a reply message.
     */
    QString msg_type = msg.value("type").toString("undefined");
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
        emit this->connexionStatus(Supercast::ConnexionSuccess);
    } else if (type == "authErr") {
        emit this->connexionStatus(Supercast::AuthenticationError);
    }
}


void Supercast::subscribe(QString channel)
{
    QJsonObject subscribeMsg {
        {"from", "supercast"},
        {"type", "subscribe"},
        {"value", QJsonObject {
                {"queryId", 0},
                {"channel", channel}}}};
    emit Supercast::singleton->clientMessage(subscribeMsg);
}


void Supercast::setMessageProcessor(QString key, SupercastSignal* dest)
{
    Supercast::singleton->message_processors->insert(key, dest);
}

void Supercast::sendQuery(QJsonObject query, SupercastSignal *reply)
{
    QMap<int, SupercastSignal*>* squeries = Supercast::singleton->queries;

    int queryId = 0;
    while (squeries->contains(queryId)) queryId += 1;

    squeries->insert(queryId, reply);
    query.insert("queryId", queryId);
    emit Supercast::singleton->clientMessage(query);
}
