#include "supercast.h"

Supercast* Supercast::singleton = NULL;
Supercast* Supercast::getInstance() {return singleton;}

Supercast::Supercast(QObject* parent) : QObject(parent)
{
    Supercast::singleton = this;
    SupercastSignal* sig = new SupercastSignal(this);
    QObject::connect(
                sig,  SIGNAL(sendMessage(QJsonObject)),
                this, SLOT(handleSupercastMessage(QJsonObject)));

    this->message_processors = new QHash<QString, SupercastSignal*>();
    this->message_processors->insert("supercast", sig);
}

void Supercast::tryConnect(
        QHostAddress host,
        qint16       port,
        QString      user_name,
        QString      user_pass)
{
    this->user_name = user_name;
    this->user_pass = user_pass;
    this->supercast_socket = new SupercastSocket(host,port);

    // server -> client
    QObject::connect(
                this->supercast_socket, SIGNAL(serverMessage(QJsonObject)),
                this,                   SLOT(routeServerMessage(QJsonObject)),
                Qt::QueuedConnection);
    // client -> server
    QObject::connect(
                this,                   SIGNAL(clientMessage(QJsonObject)),
                this->supercast_socket, SLOT(handleClientMessage(QJsonObject)),
                Qt::QueuedConnection);

    // socket state
    qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                this->supercast_socket->socket,
                    SIGNAL(error(QAbstractSocket::SocketError)),
                this,
                    SLOT(socketError(QAbstractSocket::SocketError)),
                Qt::QueuedConnection);
    QObject::connect(
                this->supercast_socket->socket, SIGNAL(connected()),
                this,                           SLOT(socketConnected()),
                Qt::QueuedConnection);

    this->supercast_socket->moveToThread(&socket_thread);
    this->socket_thread.start();
}


Supercast::~Supercast()
{
    this->socket_thread.quit();
    this->socket_thread.wait();
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
    std::cout << "socket error: " << error << std::endl;
    emit this->connexionStatus(error);
}


void Supercast::routeServerMessage(QJsonObject msg)
{
    QString from = msg.value("from").toString("undefined");
    if (this->message_processors->contains(from)) {
        SupercastSignal* sig = this->message_processors->value(from);
        emit sig->sendMessage(msg);
    }
}


void Supercast::handleSupercastMessage(QJsonObject message)
{
    QString type = message.value("type").toString("undefined");
    qDebug() << "handle supercast message?";
    if (QString::compare(type, "authAck") == 0) {
        emit this->connexionStatus(Supercast::ConnexionSuccess);
    } else if (QString::compare(type, "authErr") == 0) {
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
