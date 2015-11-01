#ifndef MONITORCHANNEL_H
#define MONITORCHANNEL_H

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "rrds/rrd4qt.h"
#include "rrds/rrd4qtsignal.h"

#include <QObject>
#include <QDebug>
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
    QString sync_dir;
    QString channel;
    QString chan_type;
    int  subscriber_count;
    bool synchronized;
    bool locked;
    QHash<QString, QString> table_files;
    QHash<QString, bool>    table_files_update_status;
    QHash<QString, bool>    table_file_rrd_pending;
    QQueue<QJsonObject>     pending_updates;

    QTemporaryFile simple_file;

    QQueue<QJsonObject> waiting_msgs;

    QJsonObject buildDump();


public:
    void increaseSubscriberCount();
    void decreaseSubscriberCount();
    QJsonObject getDumpInfo();
    bool hasDumpInfo();

signals:
    void channelDeleted(QString channel_name);
    void channelEvent(QJsonObject event);

public slots:
    void handleServerEvent(QJsonObject    event);
    void handleRrdEventSimple(QJsonObject event);
    void handleRrdEventTable(QJsonObject  event);
    void handleHttpReplySimple(QString rep);
    void handleHttpReplyTable(QString  rep);

};

#endif // MONITORCHANNEL_H
