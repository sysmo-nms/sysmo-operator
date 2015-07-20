#ifndef MONITORCHANNEL_H
#define MONITORCHANNEL_H

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "rrds/rrd4c.h"
#include "rrds/rrd4csignal.h"

#include <QObject>
#include <QDebug>
#include <QJsonObject>
#include <QQueue>
#include <QHash>
#include <QHashIterator>
#include <QTemporaryFile>
#include <QStringList>
#include <QStringListIterator>
#include <QQueue>

class MonitorChannel : public QObject
{
    Q_OBJECT
public:
    explicit MonitorChannel(QString channel, QObject *parent = 0);
    ~MonitorChannel();

private:
    QString channel;
    int  subscriber_count = 0;
    bool synchronized     = false;
    QHash<QString, QString> table_files;
    QHash<QString, bool>    table_files_update_status;
    QHash<QString, bool>    table_file_rrd_pending;
    QQueue<QJsonObject>     pending_updates;

    QTemporaryFile simple_file;

    QQueue<QJsonObject> waiting_msgs;


public:
    void increaseSubscriberCount();
    void decreaseSubscriberCount();
    QJsonObject getDumpInfo();

signals:
    void channelDeleted(QString channel_name);

public slots:
    void handleServerEvent(QJsonObject event);
    void handleRrdEventSimple(QJsonObject event);
    void handleRrdEventTable(QJsonObject  event);
    void handleHttpReplySimple(QString rep);
    void handleHttpReplyTable(QString  rep);

};

#endif // MONITORCHANNEL_H
