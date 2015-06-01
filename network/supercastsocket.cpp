#include "supercastsocket.h"

SupercastSocket::SupercastSocket(QObject *parent) : QObject(parent)
{
    std::cout << "init socket" << std::endl;
   block_size = 0;

    socket = new QTcpSocket();
    QObject::connect(
                socket, SIGNAL(connected()),
                this,   SLOT(socketConnected()));
    QObject::connect(
                socket, SIGNAL(readyRead()),
                this,   SLOT(socketReadyRead()));
    QObject::connect(
                socket, SIGNAL(error(QAbstractSocket::SocketError)),
                this,   SLOT(socketError(QAbstractSocket::SocketError)));
    socket->connectToHost(
                QHostAddress(QString("192.168.0.11")), quint16(8888));

}

void SupercastSocket::socketConnected()
{

}

void SupercastSocket::socketReadyRead()
{
    std::cout << "ready read?" << std::endl;
    QDataStream stream(socket);

    if (block_size == 0) {
        /*
         * read headear to have the content len
         */

        if (socket->bytesAvailable() < HEADER_LEN) return;

        char header_buffer[(int)HEADER_LEN];
        stream.readRawData(header_buffer, (int)HEADER_LEN);

        block_size =
                (header_buffer[0] << 24) +
                (header_buffer[1] << 16) +
                (header_buffer[2] << 8) +
                header_buffer[3];

    }

    /*
     * only read when all data is ready
     */
    if (socket->bytesAvailable() < block_size) return;

    /*
     * get payload_bytes. Carefull, no null terminator:
     * specify block_size when working on it.
     */
    char payload_bytes[block_size];
    stream.readRawData(payload_bytes, block_size);

    /*
     * load payload in a QJsonObject
     */
    QByteArray    json_arr(payload_bytes, block_size);
    QJsonDocument doc = QJsonDocument::fromJson(json_arr);
    QJsonObject   json_obj = doc.object();

    std::cout << "fromJson" << std::endl;
    std::cout << json_arr.toStdString() << std::endl;
    std::cout << json_obj.value(QString("type")).toString(QString("")).toStdString() << std::endl;

    block_size = 0;

    emit this->serverMessage(json_obj);
}

void SupercastSocket::socketError(QAbstractSocket::SocketError err)
{
    std::cout << "error is: ";
    std::cout << err << std::endl;

}

SupercastSocket::~SupercastSocket()
{
    socket->close();
}
