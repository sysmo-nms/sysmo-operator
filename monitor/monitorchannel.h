#ifndef MONITORCHANNEL_H
#define MONITORCHANNEL_H

#include "network/supercast.h"
#include "network/supercastsignal.h"

#include <QObject>
#include <QDebug>
#include <QJsonObject>
#include <QQueue>
#include <QHash>
#include <QTemporaryFile>

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
    bool simple_type      = false;
    QHash<QString, QTemporaryFile> table_files;
    QTemporaryFile simple_file;

    QQueue<QJsonObject> waiting_msgs;

signals:
    void channelDeleted(QString channel_name);

public slots:
    void handleServerEvent(QJsonObject event);
    void httpReply(QString rep);

};

#endif // MONITORCHANNEL_H
