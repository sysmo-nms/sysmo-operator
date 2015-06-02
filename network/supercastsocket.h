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
#include <QIODevice>

class SupercastSocket : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSocket(QHostAddress host, qint16 port);
    ~SupercastSocket();
    QTcpSocket *socket;

public slots:
    void handleClientMessage(QJsonObject msg);

private:
    qint64 block_size;
    static const qint64 HEADER_LEN = 4;

private slots:
    void socketReadyRead();

signals:
    void serverMessage(QJsonObject msg);
};

#endif // SUPERCASTSOCKET_H
