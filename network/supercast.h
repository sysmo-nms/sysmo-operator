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
    static const int ConnectionSuccess   = 100;
    static const int AuthenticationError = 101;

    // API
    static void subscribe(QString     channel, SupercastSignal* subscriber);
    static void sendQuery(QJsonObject query,   SupercastSignal* reply);
    static void httpGet(QString path, SupercastSignal* reply);
    static void httpGet(QString path, QString dst_file, SupercastSignal* reply);

    // get
    static Supercast* getInstance();

public slots:
    void routeServerMessage(QJsonObject msg);
    void socketConnected();
    void socketError(QAbstractSocket::SocketError error);

private:
    static Supercast* singleton;
    static const int QUERYID_UNDEF = 100;
    QString user_name;
    QString user_pass;
    QUrl    data_base_url;
    QHash<QString, SupercastSignal*>* channels      = NULL;
    QHash<int,     SupercastSignal*>* queries       = NULL;
    QHash<int,     SupercastSignal*>* http_requests = NULL;

private slots:
    void handleSupercastMessage(QJsonObject message);
    void handleHttpReply(SupercastHttpReply reply);

signals:
    void clientMessage(QJsonObject msg);
    void clientHttpRequest(SupercastHttpRequest request);
    void connectionStatus(int status);
};

#endif // SUPERCAST_H
