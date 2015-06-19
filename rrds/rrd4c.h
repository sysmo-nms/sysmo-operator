#ifndef RRD4C_H
#define RRD4C_H

#include "rrds/rrd4csocket.h"
#include "rrds/rrd4csignal.h"

#include <QObject>
#include <QJsonObject>
#include <QThread>
#include <QAbstractSocket>
#include <QJsonObject>
#include <QJsonValue>
#include <QStringList>
#include <QHash>

#include <QDebug>


class Rrd4c : public QObject
{
    Q_OBJECT

    QThread socket_thread;

public:
    explicit Rrd4c(QObject* parent = 0);
    ~Rrd4c();
    void tryConnect(
            QHostAddress host,
            qint16       port);
    static const int ConnectionSuccess   = 100;
    static const int AuthenticationError = 101;

    static void sendQuery(QJsonObject query, Rrd4cSignal* reply);
    static Rrd4c* getInstance();

public slots:
    void socketError(QAbstractSocket::SocketError error);
    void socketConnected();

private:
    static Rrd4c* singleton;
    QHash<int,     Rrd4cSignal*>* queries            = NULL;

private slots:
    void routeServerMessage(QJsonObject msg);

signals:
    void clientMessage(QJsonObject msg);
    void connectionStatus(int status);
    // messages for the monitor proxy
    void monitorServerMessage(QJsonObject msg);
};

#endif // RRD4C_H
