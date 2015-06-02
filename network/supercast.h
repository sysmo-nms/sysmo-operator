#ifndef SUPERCAST_H
#define SUPERCAST_H

#include "iostream"

#include "network/supercastsocket.h"
#include <QObject>
#include <QJsonObject>
#include <QThread>
#include <QAbstractSocket>
#include <QJsonObject>
#include <QJsonValue>

class Supercast : public QObject
{
    Q_OBJECT

    QThread socket_thread;

public:
    explicit Supercast(
            QHostAddress host,
            qint16       port,
            QString      user_name,
            QString      user_pass,
            QObject     *parent = 0);
    ~Supercast();
    QString user_name;
    QString user_pass;

public slots:
    void handleServerMessage(QJsonObject msg);
    void socketConnected();
    void socketError(QAbstractSocket::SocketError error);

private:
    SupercastSocket *supercast_socket;

signals:
    void clientMessage(QJsonObject msg);
};

#endif // SUPERCAST_H
