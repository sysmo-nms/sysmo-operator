#ifndef SUPERCAST_H
#define SUPERCAST_H

#include "iostream"

#include "network/supercastsocket.h"
#include <QObject>
#include <QJsonObject>
#include <QThread>

class Supercast : public QObject
{
    Q_OBJECT

    QThread socket_thread;

public:
    explicit Supercast(QObject *parent = 0);
    ~Supercast();

public slots:
    void handleServerMessage(QJsonObject msg);

private:
    SupercastSocket *supercast_socket;

signals:
    void clientMessage(QJsonObject msg);
};

#endif // SUPERCAST_H
