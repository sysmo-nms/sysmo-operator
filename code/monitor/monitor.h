/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
#ifndef MONITOR_H
#define MONITOR_H
#include <QWidget>
#include <QString>
#include <QVariant>
#include <QObject>
#include <QMap>
#include "monitorchannel.h"

class MonitorProxyWidget : public QWidget {
    Q_OBJECT
protected:
    QString my_channel;

public:
    explicit MonitorProxyWidget(QString channel, QWidget *parent = 0);
    ~MonitorProxyWidget();

public slots:
    virtual void handleEvent(QVariant) = 0;
    void connectToChannel();

signals:
    void connectMe();

};

class Monitor : public QObject {
    Q_OBJECT
public:
    explicit Monitor(QObject *parent = 0);
    ~Monitor();
    static Monitor* getInstance();
    QMap<QString, QVariant>* targets;
    QMap<QString, QVariant>* probes;
    QMap<QString, MonitorChannel*>* channels;
    static void subscribeToChannel(
            QString channel, MonitorProxyWidget* subscriber);
    static void unsubscribeToChannel(
            QString channel, MonitorProxyWidget* subscriber);
    static QVariant getTarget(QString targetId);
    static QVariant getProbe(QString probeId);
    static QWidget* getCenterWidget();

private:
    static Monitor* singleton;

public slots:
    void handleServerMessage(QVariant message);
    void channelDeleted(QString chan_name);

signals:
    void infoProbe(QVariant message);
    void infoTarget(QVariant message);
    void deleteTarget(QVariant message);
    void deleteProbe(QVariant message);
    void probeReturn(QVariant message);
    void initialSyncBegin(QVariant message);
    void initialSyncEnd();
    void dbNotification(QVariant message);

};

#endif // MONITOR_H
