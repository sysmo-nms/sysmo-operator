/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

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
#ifndef SUPERCASTWEBSOCKET_H
#define SUPERCASTWEBSOCKET_H
#include <QObject>
#include <QHostAddress>
#include <QWebSocket>
#include <QVariant>
#include <QAbstractSocket>
#include <QByteArray>
#include <QTimer>

class SupercastWebSocket : public QObject {
    Q_OBJECT

public:
    explicit SupercastWebSocket(QHostAddress host, qint16 port);
    ~SupercastWebSocket();
    QWebSocket* socket;

public slots:
    void handleClientMessage(QVariant msg);
    void timerTimeout();
    void handleSocketError(QAbstractSocket::SocketError error);
    void threadStarted();

private:
    static qint32 arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32 source);
    QHostAddress host;
    qint16 port;
    QTimer* timer;

private slots:
    void handleTextMessage(const QString &message);

signals:
    void serverMessage(QVariant msg);
    void waitTimeout(int error);
    void socketError(int error);
};

#endif // SUPERCASTWEBSOCKET_H
