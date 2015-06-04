#ifndef SUPERCASTSOCKET_H
#define SUPERCASTSOCKET_H

#include "iostream"
#include "stdlib.h"

#include <QObject>
#include <QJsonDocument>
#include <QJsonObject>
#include <QStringList>
#include <QTcpSocket>
#include <QAbstractSocket>
#include <QDataStream>
#include <QHostAddress>
#include <QIODevice>
#include <Qt>

class SupercastSocket : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSocket(QHostAddress host, qint16 port);
    ~SupercastSocket();
    QTcpSocket* socket;

public slots:
    void handleClientMessage(QJsonObject msg);

private:
    qint32 block_size;
    static const qint32 HEADER_LEN = 4;
    static qint32     arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32 source);

private slots:
    void socketReadyRead();

signals:
    void serverMessage(QJsonObject msg);
};

#endif // SUPERCASTSOCKET_H
