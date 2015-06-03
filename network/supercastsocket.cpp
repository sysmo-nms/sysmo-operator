#include "supercastsocket.h"

SupercastSocket::SupercastSocket(QHostAddress host, qint16 port) : QObject()
{
    this->block_size = 0;
    this->socket = new QTcpSocket(this);

    QObject::connect(
                this->socket, SIGNAL(readyRead()),
                this,         SLOT(socketReadyRead()),
                Qt::QueuedConnection);

    this->socket->connectToHost(host, port);
}


SupercastSocket::~SupercastSocket()
{
    this->socket->close();
}


void SupercastSocket::socketReadyRead()
{
    /*
     * First cancel duplicate readyRead() signals.
     * (see end of function)
     */
    if (this->socket->bytesAvailable() == 0) return;

    if (this->block_size == 0) {
        /*
         * read header to set block_size
         */
        if (this->socket->bytesAvailable() < HEADER_LEN) return;

        QByteArray header = this->socket->read(HEADER_LEN);
        this->block_size = SupercastSocket::arrayToInt(header);
    }


    /*
     * only read when all data is ready
     */
    if (this->socket->bytesAvailable() < this->block_size) {
        return;
    }


    /* OK read data */
    /*
     * get payload_bytes. Carefull, no null terminator:
     * specify this->block_size when working on it.
     */
    QByteArray    payload  = this->socket->read(this->block_size);
    QJsonDocument json_doc = QJsonDocument::fromJson(payload);
    QJsonObject   json_obj = json_doc.object();
    std::cout << "json msg: " << json_doc.toJson().data() << std::endl;
    // Deliver the message
    emit this->serverMessage(json_obj);

    /*
     * Reinitialize block size to 0
     */
    this->block_size = 0;

    /*
     * Is there some data buffered?
     * Some PDUs might comme in one readyRead() signal. We must trigger it
     * again.
     */
    if ((int)this->socket->bytesAvailable() != 0)
        emit this->socket->readyRead();
}


void SupercastSocket::handleClientMessage(QJsonObject msg)
{
    QByteArray  json_array(QJsonDocument(msg).toJson(QJsonDocument::Compact));
    qint32      json_size((qint32)json_array.size());
    this->socket->write(SupercastSocket::intToArray(json_size));
    this->socket->write(json_array.data(), json_size);
}

qint32 SupercastSocket::arrayToInt(QByteArray source)
{
    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;
}

QByteArray SupercastSocket::intToArray(qint32 source)
{
    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;
}
