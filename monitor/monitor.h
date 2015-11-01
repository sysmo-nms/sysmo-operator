#ifndef MONITOR_H
#define MONITOR_H

#include "network/supercast.h"
#include "monitor/monitorchannel.h"
#include "qjson.h"

#include <QObject>
#include <QWidget>
#include <QMap>
#include <QString>
#include <QVariant>

#include <QDebug>


class MonitorProxyWidget : public QWidget
{
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


class Monitor : public QObject
{
    Q_OBJECT
public:
    explicit Monitor(QObject *parent = 0);
    ~Monitor();
    static Monitor* getInstance();
    QMap<QString, QVariant>*     targets;
    QMap<QString, QVariant>*     probes;
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
