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
#include "supercastsocket.h"


SupercastSocket::SupercastSocket(QHostAddress host, qint16 port) : QObject()
{

    this->block_size = 0;
    this->socket     = new SupercastTcpSocket(this);
    this->host = host;
    this->port = port;

    QObject::connect(
                this->socket, SIGNAL(error(QAbstractSocket::SocketError)),
                this, SLOT(handleSocketError(QAbstractSocket::SocketError)));


    /*
     * QueuedConnection because the SLOT may emit the SIGNAL he is
     * connected to.
     */
    QObject::connect(
                this->socket, SIGNAL(readyRead()),
                this,         SLOT(socketReadyRead()),
                Qt::QueuedConnection);

}


void SupercastSocket::threadStarted()
{

    QTimer *timer = new QTimer(this);
    timer->setSingleShot(true);
    timer->setInterval(Sysmo::SUPERCAST_SOCKET_TIMEOUT);

    QObject::connect(
                timer, SIGNAL(timeout()),
                this, SLOT(timerTimeout()),
                Qt::QueuedConnection);

    timer->start();
    this->socket->connectToHost(this->host, this->port);

}


SupercastSocket::~SupercastSocket()
{

    this->socket->close();

}


void SupercastSocket::timerTimeout()
{

    if (this->socket->state() == QAbstractSocket::UnconnectedState) return;
    if (this->socket->state() != QAbstractSocket::ConnectedState) {
        emit this->waitTimeout(QAbstractSocket::NetworkError);
        this->socket->abort();
    }

}


void SupercastSocket::socketReadyRead()
{

    /*
     * read header to set block_size. Only read when the header is
     * complete.
     */
    if (this->block_size == 0)
    {
        if (this->socket->bytesAvailable() < HEADER_LEN) return;

        QByteArray header = this->socket->read(HEADER_LEN);
        this->block_size = SupercastSocket::arrayToInt32(header);
    }


    /*
     * We have the block_size. Only read when the payload is complete.
     */
    if (this->socket->bytesAvailable() < this->block_size) return;


    /*
     * Read and decode the payload.
     */
    QByteArray payload = this->socket->read(this->block_size);
    QVariant   json_obj = QJson::decode(QString(payload));


    /*
     * Deliver the message
     */
    emit this->serverMessage(json_obj);


    /*
     * Reinitialize block size to 0
     */
    this->block_size = 0;


    /*
     * Emit aditional readyRead() wich will call this function again
     * without recursion (QueuedConnection).
     */
    if (this->socket->bytesAvailable() != 0)
        this->socket->emitReadyRead();

}


void SupercastSocket::handleClientMessage(QVariant msg)
{

    QByteArray json_array = QJson::encode(msg).toLatin1();
    qDebug() << "will sed:" << json_array;
    qint32     json_size(json_array.size());
    qDebug() << "will send size:" << json_array.size();
    this->socket->write(SupercastSocket::int32ToArray(json_size));
    this->socket->write(json_array.data(), json_size);
    qDebug() << "have sent size:" << json_array.data();

}


qint32 SupercastSocket::arrayToInt32(QByteArray source)
{

    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;

}


QByteArray SupercastSocket::int32ToArray(qint32 source)
{

    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;

}


void SupercastSocket::handleSocketError(QAbstractSocket::SocketError error) {

    emit this->socketError((int) error);

}


SupercastTcpSocket::SupercastTcpSocket(QObject *parent) : QTcpSocket(parent)
{

}

void SupercastTcpSocket::emitReadyRead()
{

    emit this->readyRead();
   
}
