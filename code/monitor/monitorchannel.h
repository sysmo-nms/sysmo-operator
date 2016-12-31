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
#ifndef MONITORCHANNEL_H
#define MONITORCHANNEL_H

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "rrds/rrd4qt.h"
#include "rrds/rrd4qtsignal.h"

#include <QObject>
#include <QDebug>
#include <QQueue>
#include <QMap>
#include <QMapIterator>
#include <QTemporaryFile>
#include <QStringList>
#include <QStringListIterator>
#include <QQueue>
#include <QVariant>

class MonitorChannel : public QObject
{
    Q_OBJECT
public:
    explicit MonitorChannel(QString channel, QObject *parent = 0);
    ~MonitorChannel();

private:
    QString sync_dir;
    QString channel;
    QString chan_type;
    int  subscriber_count;
    bool synchronized;
    bool locked;
    QMap<QString, QString> table_files;
    QMap<QString, bool>    table_files_update_status;
    QMap<QString, bool>    table_file_rrd_pending;
    QQueue<QVariant>     pending_updates;

    QTemporaryFile simple_file;

    QQueue<QVariant> waiting_msgs;

    QMap<QString,QVariant> buildDump();


public:
    void increaseSubscriberCount();
    void decreaseSubscriberCount();
    QMap<QString,QVariant> getDumpInfo();
    bool hasDumpInfo();

signals:
    void channelDeleted(QString channel_name);
    void channelEvent(QVariant event);

public slots:
    void handleServerEvent(QVariant    event);
    void handleRrdEventSimple(QVariant event);
    void handleRrdEventTable(QVariant  event);
    void handleHttpReplySimple(QString rep);
    void handleHttpReplyTable(QString  rep);

};

#endif // MONITORCHANNEL_H
