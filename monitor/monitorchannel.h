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
