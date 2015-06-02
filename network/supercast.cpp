#include "supercast.h"


Supercast::Supercast(QObject *parent) : QObject(parent)
{
    this->supercast_socket = new SupercastSocket();
    this->supercast_socket->moveToThread(&socket_thread);
    QObject::connect(
                this->supercast_socket, SIGNAL(serverMessage(QJsonObject)),
                this,                   SLOT(handleServerMessage(QJsonObject)),
                Qt::QueuedConnection);
    QObject::connect(
                this,                   SIGNAL(clientMessage(QJsonObject)),
                this->supercast_socket, SLOT(handleClientMessage(QJsonObject)),
                Qt::QueuedConnection);
    this->socket_thread.start();
}


Supercast::~Supercast()
{
    this->socket_thread.quit();
    this->socket_thread.wait();
}


void Supercast::handleServerMessage(QJsonObject msg)
{
    std::cout << "helolololo" << std::endl;
    std::cout << msg.value(QString("type")).toString(QString("")).toStdString() << std::endl;
    emit this->clientMessage(msg);
}
