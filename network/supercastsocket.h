#ifndef SUPERCASTSOCKET_H
#define SUPERCASTSOCKET_H

#include "sysmo.h"
#include "qjson.h"

#include <QObject>
#include <QStringList>
#include <QTcpSocket>
#include <QAbstractSocket>
#include <QDataStream>
#include <QHostAddress>
#include <QIODevice>
#include <Qt>
#include <QTimer>
#include <QVariant>

class SupercastTcpSocket : public QTcpSocket
{
public:
    explicit SupercastTcpSocket(QObject* parent = 0);
    void emitReadyRead();
};

class SupercastSocket : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSocket(QHostAddress host, qint16 port);
    ~SupercastSocket();
    SupercastTcpSocket* socket;

public slots:
    void handleClientMessage(QVariant msg);
    void timerTimeout();
    void handleSocketError(QAbstractSocket::SocketError error);

private:
    qint32 block_size;
    static const int HEADER_LEN = 4;

    static qint32     arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32 source);

private slots:
    void socketReadyRead();

signals:
    void serverMessage(QVariant msg);
    void waitTimeout(int error);
    void socketError(int error);
};

#endif // SUPERCASTSOCKET_H
