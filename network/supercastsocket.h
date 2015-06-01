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
    explicit SupercastSocket(QObject *parent = 0);
    ~SupercastSocket();

public slots:

signals:
    void serverMessage(QJsonObject msg);

private:
    QTcpSocket *socket;
    qint64     block_size;
    static const qint64 HEADER_LEN = 4;

private slots:
    void socketReadyRead();
    void socketConnected();
    void socketError(QAbstractSocket::SocketError err);
};

#endif // SUPERCASTSOCKET_H
