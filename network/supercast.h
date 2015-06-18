#ifndef SUPERCAST_H
#define SUPERCAST_H

#include "network/supercastsocket.h"
#include "network/supercastsignal.h"
#include "network/supercasthttp.h"
#include "network/supercasthttprequest.h"
#include "network/supercasthttpreply.h"

#include <QObject>
#include <QJsonObject>
#include <QThread>
#include <QAbstractSocket>
#include <QJsonObject>
#include <QJsonValue>
#include <QStringList>
#include <QHash>

#include <QDebug>


class Supercast : public QObject
{
    Q_OBJECT

    QThread socket_thread;
    QThread http_thread;

public:
    explicit Supercast(QObject* parent = 0);
    ~Supercast();
    void tryConnect(
            QHostAddress host,
            qint16       port,
            QString      user_name,
            QString      user_pass);
    QString user_name;
    QString user_pass;
    QString testouille;
    QHash<QString, SupercastSignal*>* message_processors = NULL;
    QHash<int, SupercastSignal*>*      queries            = NULL;
    QHash<int, SupercastSignal*>*      http_requests      = NULL;
    static const int ConnexionSuccess    = 100;
    static const int AuthenticationError = 101;
    static Supercast* getInstance();
    static void subscribe(QString channel);
    static void setMessageProcessor(QString key, SupercastSignal* dest);
    static void sendQuery(QJsonObject query, SupercastSignal* reply);
    static void httpGet(QString url, SupercastSignal* reply);

public slots:
    void routeServerMessage(QJsonObject msg);
    void socketConnected();
    void socketError(QAbstractSocket::SocketError error);

private:
    static Supercast* singleton;
    static const int QUERYID_UNDEF = 100;

private slots:
    void handleSupercastMessage(QJsonObject message);
    void handleHttpReply(SupercastHttpReply reply);

signals:
    void clientMessage(QJsonObject msg);
    void clientHttpRequest(SupercastHttpRequest request);
    void connexionStatus(int status);
    // messages for the monitor proxy
    void monitorServerMessage(QJsonObject msg);
};

#endif // SUPERCAST_H
