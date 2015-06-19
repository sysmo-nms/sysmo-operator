#include "rrd4csocket.h"

Rrd4cSocket::Rrd4cSocket(QHostAddress host, qint16 port) : QObject()
{
    this->block_size = 0;
    this->socket     = new QTcpSocket(this);

    /*
     * QueuedConnection because the SLOT may emit the SIGNAL he is
     * connected to.
     */
    QObject::connect(
                this->socket, SIGNAL(readyRead()),
                this,         SLOT(socketReadyRead()),
                Qt::QueuedConnection);

    this->socket->connectToHost(host, port);
}


Rrd4cSocket::~Rrd4cSocket()
{
    this->socket->close();
}


void Rrd4cSocket::socketReadyRead()
{
    /*
     * read header to set block_size. Only read when the header is
     * complete.
     */
    if (this->block_size == 0) {
        if (this->socket->bytesAvailable() < HEADER_LEN) return;

        QByteArray header = this->socket->read(HEADER_LEN);
        this->block_size = Rrd4cSocket::arrayToInt32(header);
    }


    /*
     * We have the block_size. Only read when the payload is complete.
     */
    if (this->socket->bytesAvailable() < this->block_size) return;


    /*
     * Read and decode the payload.
     */
    QByteArray    payload  = this->socket->read(this->block_size);
    QJsonDocument json_doc = QJsonDocument::fromJson(payload);
    QJsonObject   json_obj = json_doc.object();


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
        emit this->socket->readyRead();
}


void Rrd4cSocket::handleClientMessage(QJsonObject msg)
{
    QByteArray  json_array(QJsonDocument(msg).toJson(QJsonDocument::Compact));
    qint32      json_size(json_array.size());
    this->socket->write(Rrd4cSocket::int32ToArray(json_size));
    this->socket->write(json_array.data(), json_size);
}

qint32 Rrd4cSocket::arrayToInt32(QByteArray source)
{
    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;
}

QByteArray Rrd4cSocket::int32ToArray(qint32 source)
{
    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;
}
