/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
#ifndef SUPERCAST_H
#define SUPERCAST_H

#include "supercastsignal.h"
#include "supercasthttp.h"
#include "supercasthttprequest.h"
#include "supercasthttpreply.h"

#ifdef USE_WEBSOCKET
#include "supercastwebsocket.h"
#else
#include "supercastsocket.h"
#endif

#include <QObject>
#include <QThread>
#include <QAbstractSocket>
#include <QStringList>
#include <QMap>
#include <QVariant>

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
    static const int CONNECTION_SUCCESS   = 100;
    static const int AUTHENTICATION_ERROR = 101;

    // API
    static void subscribe(QString channel, SupercastSignal* subscriber);
    static void unsubscribe(QString channel);
    static void sendQuery(QVariant query,   SupercastSignal* reply);
    static void httpGet(QString path, SupercastSignal* reply);
    static void httpGet(QString path, QString dst_file, SupercastSignal* reply);
    static void httpGet(QString path, QString dst_file, SupercastSignal* reply, QString opaque);

    // singleton
    static Supercast* getInstance();

public slots:
    void routeServerMessage(QVariant msg);
    void socketConnected();
    void socketError(int error);

private:
    static Supercast* singleton;
    static const int QUERYID_UNDEF = 100;
    QString user_name;
    QString user_pass;
    QUrl    data_base_url;
    QMap<QString, SupercastSignal*>* channels;
    QMap<int,     SupercastSignal*>* queries;
    QMap<int,     SupercastSignal*>* http_requests;

private slots:
    void handleSupercastMessage(QVariant message);
    void handleHttpReply(SupercastHttpReply reply);

signals:
    void clientMessage(QVariant msg);
    void clientHttpRequest(SupercastHttpRequest request);
    void connectionStatus(int status);
};

#endif // SUPERCAST_H
