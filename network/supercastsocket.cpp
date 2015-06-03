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
    if ((int)this->socket->bytesAvailable() == 0) return;

    QDataStream stream(this->socket);

    if (this->block_size == 0) {
        /*
         * read header to have the content len
         */

        if (this->socket->bytesAvailable() < HEADER_LEN) return;

        char head_buffer[(int)HEADER_LEN];
        stream.readRawData(head_buffer, (int)HEADER_LEN);

        /*
         * XXX Big endian problem?
         */
        this->block_size =
            (head_buffer[0] << 24) +
            (head_buffer[1] << 16) +
            (head_buffer[2] <<  8) +
             head_buffer[3];
    }

    /*
     * only read when all data is ready
     */
    if (this->socket->bytesAvailable() < this->block_size) return;


    /* OK read data */
    /*
     * get payload_bytes. Carefull, no null terminator:
     * specify this->block_size when working on it.
     */
    char payload_bytes[this->block_size];
    stream.readRawData(payload_bytes, this->block_size);

    /*
     * load payload in a QJsonObject
     */
    QByteArray    json_arr(payload_bytes, this->block_size);
    QJsonDocument json_doc = QJsonDocument::fromJson(json_arr);
    QJsonObject   json_obj = json_doc.object();

    std::cout << "json msg: " << json_doc.toJson().data() << std::endl;

    /*
     * Reinitialize nex block size to 0
     */
    this->block_size = 0;

    /*
     * Deliver the message
     */
    emit this->serverMessage(json_obj);

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

    /*
     * build the four bytes header with json_size
     * TODO: maybe use QDataStream
     * XXX Big endian problem?
     */
    char header_buffer[HEADER_LEN];
    header_buffer[0] = (json_size >> 24) & 0xff;
    header_buffer[1] = (json_size >> 16) & 0xff;
    header_buffer[2] = (json_size >> 8)  & 0xff;
    header_buffer[3] =  json_size        & 0xff;

    this->socket->write(header_buffer, HEADER_LEN);
    this->socket->write(json_array.data(), (qint64)json_size);
}
