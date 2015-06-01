#ifndef SUPERCASTSOCKET_H
#define SUPERCASTSOCKET_H

#include "iostream"

#include <QObject>
#include <QJsonDocument>
#include <QJsonObject>
#include <QStringList>
#include <QTcpSocket>
#include <QAbstractSocket>
#include <QDataStream>
#include <QHostAddress>

class SupercastSocket : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSocket();
    ~SupercastSocket();

public slots:
    void handleClientMessage(QJsonObject msg);

private:
    QTcpSocket *socket;
    qint64     block_size;
    static const qint64 HEADER_LEN = 4;

private slots:
    void socketReadyRead();
    void socketConnected();
    void socketError(QAbstractSocket::SocketError err);

signals:
    void serverMessage(QJsonObject msg);
};

#endif // SUPERCASTSOCKET_H
