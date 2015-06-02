#include "supercast.h"


Supercast::Supercast(
        QHostAddress host,
        qint16       port,
        QString      user_name,
        QString      user_pass,
        QObject     *parent) : QObject(parent)
{
    this->user_name = user_name;
    this->user_pass = user_pass;
    this->supercast_socket = new SupercastSocket(host,port);

    // server -> client
    QObject::connect(
                this->supercast_socket, SIGNAL(serverMessage(QJsonObject)),
                this,                   SLOT(handleServerMessage(QJsonObject)),
                Qt::QueuedConnection);
    // client -> server
    QObject::connect(
                this,                   SIGNAL(clientMessage(QJsonObject)),
                this->supercast_socket, SLOT(handleClientMessage(QJsonObject)),
                Qt::QueuedConnection);

    // socket state
    qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                this->supercast_socket->socket, SIGNAL(error(QAbstractSocket::SocketError)),
                this,                           SLOT(socketError(QAbstractSocket::SocketError)),
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
}


void Supercast::handleServerMessage(QJsonObject msg)
{
    std::cout << "helolololo" << std::endl;
    std::cout << msg.value(QString("type")).toString(QString("")).toStdString() << std::endl;
    //emit this->clientMessage(msg);
}
