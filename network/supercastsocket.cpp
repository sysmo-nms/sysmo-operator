#include "supercastsocket.h"


SupercastSocket::SupercastSocket(QHostAddress host, qint16 port)
        : QObject()
{
    this->block_size = 0;
    this->socket = new QTcpSocket(this);

    QObject::connect(
                this->socket, SIGNAL(readyRead()),
                this,         SLOT(socketReadyRead()));

    this->socket->connectToHost(host, port);
}


SupercastSocket::~SupercastSocket()
{
    this->socket->close();
}


void SupercastSocket::socketReadyRead()
{
    QDataStream stream(this->socket);

    if (this->block_size == 0) {
        /*
         * read header to have the content len
         */

        if (this->socket->bytesAvailable() < HEADER_LEN) return;

        char head_buffer[(int)HEADER_LEN];
        stream.readRawData(head_buffer, (int)HEADER_LEN);

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
    emit this->serverMessage(json_obj);
    this->block_size = 0;
}


void SupercastSocket::handleClientMessage(QJsonObject msg)
{
    QByteArray  json_array(QJsonDocument(msg).toJson(QJsonDocument::Compact));
    qint32      json_size((qint32)json_array.size());

    /*
     * build the four bytes header with json_size
     * TODO: maybe use QDataStream
     */
    char header_buffer[HEADER_LEN];
    header_buffer[0] = (json_size >> 24) & 0xff;
    header_buffer[1] = (json_size >> 16) & 0xff;
    header_buffer[2] = (json_size >> 8)  & 0xff;
    header_buffer[3] =  json_size        & 0xff;

    this->socket->write(header_buffer, HEADER_LEN);
    this->socket->write(json_array.data(), (qint64)json_size);
}
