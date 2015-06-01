#include "supercastsocket.h"


SupercastSocket::SupercastSocket() : QObject()
{
    this->block_size = 0;
    this->socket     = new QTcpSocket(this);

    QObject::connect(
                this->socket, SIGNAL(connected()),
                this,         SLOT(socketConnected()));
    QObject::connect(
                this->socket, SIGNAL(readyRead()),
                this,         SLOT(socketReadyRead()));
    // !!!
    qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                this->socket, SIGNAL(error(QAbstractSocket::SocketError)),
                this,         SLOT(socketError(QAbstractSocket::SocketError)));

    this->socket->connectToHost(
        QHostAddress(QString("192.168.0.11")), quint16(8888));
}


void SupercastSocket::handleClientMessage(QJsonObject msg)
{
    QByteArray json_arr = QJsonDocument(msg).toJson();
    std::cout << "received client message" << std::endl;
    std::cout << QString(json_arr).toStdString() << std::endl;
}


void SupercastSocket::socketConnected()
{
    std::cout << "socket connected" << std::endl;
}


void SupercastSocket::socketReadyRead()
{
    std::cout << "ready read?" << std::endl;
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

    emit this->serverMessage(json_obj);
    this->block_size = 0;

    std::cout << "fromJson" << std::endl;
    std::cout << json_arr.toStdString() << std::endl;
    std::cout << json_obj.value(QString("type")).toString(QString("")).toStdString() << std::endl;
}


void SupercastSocket::socketError(QAbstractSocket::SocketError err)
{
    std::cout << "error is: ";
    std::cout << err << std::endl;
}


SupercastSocket::~SupercastSocket()
{
    this->socket->close();
}
