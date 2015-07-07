#include "rrd4c.h"

Rrd4c* Rrd4c::singleton = NULL;
Rrd4c* Rrd4c::getInstance() {return Rrd4c::singleton;}

Rrd4c::Rrd4c(QObject* parent) : QObject(parent)
{
    Rrd4c::singleton = this;
    this->queries    = new QHash<int, Rrd4cSignal*>();
}


void Rrd4c::tryConnect(
        QHostAddress host,
        qint16       port)
{
    Rrd4cSocket* socket_t = new Rrd4cSocket(host,port);

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


Rrd4c::~Rrd4c()
{
    this->socket_thread.quit();
    this->socket_thread.wait();

    delete this->queries;
}


/*
 * SLOTS
 */
void Rrd4c::socketConnected()
{

}


void Rrd4c::socketError(QAbstractSocket::SocketError error)
{
    emit this->connectionStatus(error);
}


void Rrd4c::routeServerMessage(QJsonObject msg)
{
    QString msg_type = msg.value("type").toString("undefined");
    if(msg_type == "reply") {

        int  queryId = msg.take("queryId").toInt(10000);
        bool lastPdu = msg.take("lastPdu").toBool(true);
        if (queryId == 10000) return;

        Rrd4cSignal* sig = this->queries->value(queryId);
        emit sig->serverMessage(msg);

        if (lastPdu) {
            this->queries->remove(queryId);
            sig->deleteLater();
        }

        return;
    }
}

void Rrd4c::sendQuery(QJsonObject query, Rrd4cSignal *reply)
{
    int queryId = 0;
    while (Rrd4c::singleton->queries->contains(queryId)) queryId += 1;

    Rrd4c::singleton->queries->insert(queryId, reply);
    query.insert("queryId", queryId);
    emit Rrd4c::singleton->clientMessage(query);
}
