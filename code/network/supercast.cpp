/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "supercast.h"

Supercast* Supercast::singleton = NULL;


Supercast* Supercast::getInstance() {return Supercast::singleton;}


Supercast::~Supercast()
{

    this->http_thread.quit();
    this->socket_thread.quit();

    this->http_thread.wait();
    this->http_thread.deleteLater();

    this->socket_thread.wait();
    this->socket_thread.deleteLater();

    QMap<QString, SupercastSignal*>::iterator c;
    for (
         c  = this->channels->begin();
         c != this->channels->end();
         ++c)
    {
        SupercastSignal* sig = c.value();
        delete sig;
    }
    delete this->channels;

    QMap<int, SupercastSignal*>::iterator q;
    for (
         q  = this->queries->begin();
         q != this->queries->end();
         ++q)
    {
        SupercastSignal* sig = q.value();
        delete sig;
    }
    delete this->queries;

    QMap<int, SupercastSignal*>::iterator h;
    for (
         h  = this->http_requests->begin();
         h != this->http_requests->end();
         ++h)
    {
        SupercastSignal* sig = h.value();
        delete sig;
    }
    delete this->http_requests;

}


Supercast::Supercast(QObject* parent) : QObject(parent)
{

    this->user_name = "";
    this->user_pass = "";
    this->data_base_url = QUrl();

    Supercast::singleton = this;
    this->channels      = new QMap<QString, SupercastSignal*>();
    this->queries       = new QMap<int, SupercastSignal*>();
    this->http_requests = new QMap<int, SupercastSignal*>();

    SupercastSignal* sig = new SupercastSignal();
    this->channels->insert("supercast", sig);
    QObject::connect(
                sig,  SIGNAL(serverMessage(QVariant)),
                this, SLOT(handleSupercastMessage(QVariant)));

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

#ifdef USE_WEBSOCKET
    SupercastWebSocket* socket_t = new SupercastWebSocket(host,port);
#else
    SupercastSocket* socket_t = new SupercastSocket(host,port);
#endif

    // server -> message -> client
    QObject::connect(
                socket_t, SIGNAL(serverMessage(QVariant)),
                this,     SLOT(routeServerMessage(QVariant)),
                Qt::QueuedConnection);
    // client -> message -> server
    QObject::connect(
                this,     SIGNAL(clientMessage(QVariant)),
                socket_t, SLOT(handleClientMessage(QVariant)),
                Qt::QueuedConnection);

    // socket state
    //qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                socket_t, SIGNAL(socketError(int)),
                this, SLOT(socketError(int)),
                Qt::QueuedConnection);
    QObject::connect(
                socket_t, SIGNAL(waitTimeout(int)),
                this,     SLOT(socketError(int)),
                Qt::QueuedConnection);

    QObject::connect(
                socket_t->socket, SIGNAL(connected()),
                this,             SLOT(socketConnected()),
                Qt::QueuedConnection);

    QObject::connect(
                &this->socket_thread, SIGNAL(started()),
                socket_t, SLOT(threadStarted()));

    socket_t->moveToThread(&this->socket_thread);

    QObject::connect(
                &this->socket_thread, SIGNAL(finished()),
                socket_t,             SLOT(deleteLater()));
    this->socket_thread.start();

}


/*
 * SLOTS
 */
void Supercast::socketConnected()
{

    QMap<QString, QVariant> authResp;
    QMap<QString, QVariant> value;
    value.insert("name", this->user_name);
    value.insert("password", this->user_pass);
    authResp.insert("from", "supercast");
    authResp.insert("type", "authResp");
    authResp.insert("value", value);


    emit this->clientMessage(QVariant(authResp));

}


void Supercast::socketError(int error)
{

    qDebug() << "conn error: " << error;
    emit this->connectionStatus(error);

}


void Supercast::routeServerMessage(QVariant variantMsg)
{

    QMap<QString, QVariant> msg = variantMsg.toMap();
    /*
     * Test if message is for a channel.
     */
    QString from = msg.value("from").toString();
    qDebug() << "from : " << msg.keys();
    if (this->channels->contains(from)) {
        SupercastSignal* sig = this->channels->value(from);

        sig->emitServerMessage(msg);
        return;
    }


    QString msg_type = msg.value("type").toString();
    qDebug() << "type : " << msg_type;
    /*
     * Then it should be a reply message or subscribe reply
     */
    if(msg_type == "reply") {

        int  queryId = msg.take("queryId").toInt();
        bool lastPdu = msg.take("lastPdu").toBool();
        if (queryId == 0) return;

        SupercastSignal* sig = this->queries->value(queryId);

        sig->emitServerMessage(msg);

        if (lastPdu) {
            this->queries->remove(queryId);
            sig->deleteLater();
        }
        return;
    }

    qCritical() << "unknown msg type: " << msg;

}


void Supercast::handleSupercastMessage(QVariant variantMsg)
{

    QMap<QString, QVariant> message = variantMsg.toMap();
    QString type = message.value("type").toString();
    if (type == "authAck")
    {
        emit this->connectionStatus(Supercast::CONNECTION_SUCCESS);
    }
    else if (type == "authErr")
    {
        emit this->connectionStatus(Supercast::AUTHENTICATION_ERROR);
    }
    else if (type == "serverInfo")
    {
        qDebug() << "server info" << message;
        QMap<QString,QVariant> val = message.value("value").toMap();
        this->data_base_url.setPort(val.value("dataPort").toInt());
        this->data_base_url.setScheme(val.value("dataProto").toString());
        qDebug() << "server data port" << val.value("dataPort").toInt();
    }
    else if (type == "subscribeOk" || type == "subscribeErr")
    {
        QString channel = message.value("value")
                                 .toMap()
                                 .value("channel")
                                 .toString();
        SupercastSignal* sig = this->channels->value(channel);

        sig->emitServerMessage(message);
    }
    else if (type == "unsubscribeOk" || type == "unsubscribeErr")
    {
        qDebug() << "unsubscribe channel: " << type;
    }
    else
    {
        qWarning() << "should handle this message?: " << message;
    }

}


void Supercast::subscribe(QString channel, SupercastSignal* subscriber)
{

    QMap<QString, QVariant> subscribeMsg;
    QMap<QString, QVariant> value;
    value.insert("queryId", 0);
    value.insert("channel", channel);
    subscribeMsg.insert("from", "supercast");
    subscribeMsg.insert("type", "subscribe");
    subscribeMsg.insert("value", value);

    Supercast::singleton->channels->insert(channel, subscriber);

    emit Supercast::singleton->clientMessage(subscribeMsg);

}


void Supercast::unsubscribe(QString channel)
{

    QMap<QString, QVariant> unsubscribeMsg;
    QMap<QString, QVariant> value;
    value.insert("queryId", 0);
    value.insert("channel", channel);
    unsubscribeMsg.insert("from", "supercast");
    unsubscribeMsg.insert("type", "unsubscribe");
    unsubscribeMsg.insert("value", value);

    SupercastSignal* sig = Supercast::singleton->channels->take(channel);
    sig->deleteLater();

    emit Supercast::singleton->clientMessage(unsubscribeMsg);

}


void Supercast::sendQuery(QVariant queryVariant, SupercastSignal *reply)
{

    QMap<QString,QVariant> query = queryVariant.toMap();
    int queryId = 1;
    while (Supercast::singleton->queries->contains(queryId)) queryId += 1;

    Supercast::singleton->queries->insert(queryId, reply);
    query.insert("queryId", queryId);

    emit Supercast::singleton->clientMessage(query);

}


void Supercast::httpGet(QString path, SupercastSignal *reply)
{

    int  queryId = 0;
    while (Supercast::singleton->http_requests->contains(queryId)) queryId += 1;

    Supercast::singleton->http_requests->insert(queryId, reply);

    QUrl url(Supercast::singleton->data_base_url);
    url.setPath(path);

    emit Supercast::singleton->clientHttpRequest(
                                        SupercastHttpRequest(queryId, url));

}


void Supercast::httpGet(QString path, QString dst_file, SupercastSignal *reply)
{

    int queryId = 0;
    while (Supercast::singleton->http_requests->contains(queryId)) queryId += 1;

    Supercast::singleton->http_requests->insert(queryId, reply);

    QUrl url(Supercast::singleton->data_base_url);
    url.setPath(path);

    emit Supercast::singleton->clientHttpRequest(
                                SupercastHttpRequest(queryId, dst_file, url));

}

void Supercast::httpGet(
        QString          path,
        QString          dst_file,
        SupercastSignal* reply,
        QString          opaque)
{

    int queryId = 0;
    while (Supercast::singleton->http_requests->contains(queryId)) queryId += 1;
    Supercast::singleton->http_requests->insert(queryId, reply);

    QUrl url(Supercast::singleton->data_base_url);
    url.setPath(path);

    emit Supercast::singleton->clientHttpRequest(
                        SupercastHttpRequest(queryId, dst_file, url, opaque));

}


void Supercast::handleHttpReply(SupercastHttpReply reply)
{

    int queryId = reply.id;
    SupercastSignal* sig = Supercast::singleton->http_requests->take(queryId);

    sig->emitServerMessage(reply.body);

    sig->deleteLater();

}
