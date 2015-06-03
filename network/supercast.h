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
#include <QStringList>


class Supercast : public QObject
{
    Q_OBJECT

    QThread socket_thread;

public:
    explicit Supercast(QObject* parent = 0);
    ~Supercast();
    void tryConnect(
            QHostAddress host,
            qint16       port,
            QString      user_name,
            QString      user_pass);
    static Supercast* getInstance();
    static void subscribe(QString channel);
    QString user_name;
    QString user_pass;
    QString testouille;
    static const int ConnexionSuccess    = 100;
    static const int AuthenticationError = 101;

public slots:
    void handleServerMessage(QJsonObject msg);
    void socketConnected();
    void socketError(QAbstractSocket::SocketError error);

private:
    SupercastSocket*  supercast_socket;
    static Supercast* singleton;

signals:
    void clientMessage(QJsonObject msg);
    void connexionStatus(int status);
    // messages for the monitor proxy
    void monitorServerMessage(QJsonObject msg);
};

#endif // SUPERCAST_H
