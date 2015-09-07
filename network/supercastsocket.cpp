#include "supercastsocket.h"

SupercastSocket::SupercastSocket(QHostAddress host, qint16 port) : QObject()
{
    this->block_size = 0;
    this->socket     = new QTcpSocket(this);

    QTimer *timer = new QTimer(this);
    timer->setSingleShot(true);
    timer->setInterval(Sysmo::SUPERCAST_SOCKET_TIMEOUT);

    QObject::connect(
                timer, SIGNAL(timeout()),
                this, SLOT(timerTimeout()),
                Qt::QueuedConnection);

    /*
     * QueuedConnection because the SLOT may emit the SIGNAL he is
     * connected to.
     */
    QObject::connect(
                this->socket, SIGNAL(readyRead()),
                this,         SLOT(socketReadyRead()),
                Qt::QueuedConnection);

    timer->start();
    this->socket->connectToHost(host, port);
}

SupercastSocket::~SupercastSocket()
{
    this->socket->close();
}

void SupercastSocket::timerTimeout()
{
    qDebug() << "timer timeoutddddddddddddddd" << this->socket->state();
    if (this->socket->state() != QAbstractSocket::ConnectedState) {
        qDebug() << "then close???";
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
    QByteArray     payload = this->socket->read(this->block_size);
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


void SupercastSocket::handleClientMessage(QJsonObject msg)
{
    QByteArray  json_array(QJsonDocument(msg).toJson(QJsonDocument::Compact));
    qint32      json_size(json_array.size());
    this->socket->write(SupercastSocket::int32ToArray(json_size));
    this->socket->write(json_array.data(), json_size);
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
