#ifndef SUPERCAST_H
#define SUPERCAST_H

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

private:
    SupercastSocket *supercast_socket;

signals:
    void serverMessage(QJsonObject msg);
};

#endif // SUPERCAST_H
