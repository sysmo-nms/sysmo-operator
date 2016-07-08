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
#include "supercastwebsocket.h"


SupercastWebSocket::SupercastWebSocket(QHostAddress host, qint16 port) : QObject()
{

    this->socket = new QWebSocket();
    this->socket->setParent(this);
    this->host = host;
    this->port = port;

    this->timer = new QTimer(this);
    this->timer->setSingleShot(true);
    this->timer->setInterval(Sysmo::SUPERCAST_SOCKET_TIMEOUT);

    QObject::connect(
                this->timer, SIGNAL(timeout()),
                this, SLOT(timerTimeout()),
                Qt::QueuedConnection);
    qRegisterMetaType<QAbstractSocket::SocketError>();
    qRegisterMetaType<QAbstractSocket::SocketState>();
    QObject::connect(
                this->socket, SIGNAL(error(QAbstractSocket::SocketError)),
                this, SLOT(handleSocketError(QAbstractSocket::SocketError)));

    QObject::connect(
                this->socket, SIGNAL(textMessageReceived(QString)),
                this,         SLOT(handleTextMessage(QString)));

}


void SupercastWebSocket::threadStarted()
{

    QString urlStr = "ws://%1:%2/websocket";
    QUrl url(urlStr.arg(this->host.toString()).arg(this->port));
    this->timer->start();
    qDebug() << "will open " << url.toString();
    this->socket->open(url);

}


SupercastWebSocket::~SupercastWebSocket()
{

    this->socket->close();

}


void SupercastWebSocket::timerTimeout()
{

    if (this->socket->state() == QAbstractSocket::UnconnectedState) return;
    if (this->socket->state() != QAbstractSocket::ConnectedState) {
        emit this->waitTimeout(QAbstractSocket::NetworkError);
        this->socket->abort();
    }

}


void SupercastWebSocket::handleTextMessage(const QString &message)
{

    QVariant json_obj = QJson::decode(message);
    emit this->serverMessage(json_obj);

}


void SupercastWebSocket::handleClientMessage(QVariant msg)
{

    //QByteArray json_array = QJson::encode(msg).toLatin1();
    this->socket->sendTextMessage(QJson::encode(msg));

}

qint32 SupercastWebSocket::arrayToInt32(QByteArray source)
{

    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;

}

QByteArray SupercastWebSocket::int32ToArray(qint32 source)
{

    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;

}

void SupercastWebSocket::handleSocketError(QAbstractSocket::SocketError error) {

    emit this->socketError((int) error);
   
}


