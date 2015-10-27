#ifndef MONITOR_H
#define MONITOR_H

#include "network/supercast.h"
#include "monitor/monitorchannel.h"

#include <QObject>
#include <QWidget>
#include <QHash>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QString>

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
    virtual void handleEvent(QJsonObject) = 0;
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
    QHash<QString, QJsonObject>*     targets;
    QHash<QString, QJsonObject>*     probes;
    QHash<QString, MonitorChannel*>* channels;
    static void subscribeToChannel(
            QString channel, MonitorProxyWidget* subscriber);
    static void unsubscribeToChannel(
            QString channel, MonitorProxyWidget* subscriber);
    static QJsonObject getTarget(QString targetId);
    static QJsonObject getProbe(QString probeId);
    static QWidget* getCenterWidget();

private:
    static Monitor* singleton;

public slots:
    void handleServerMessage(QJsonObject message);
    void channelDeleted(QString chan_name);

signals:
    void infoProbe(QJsonObject message);
    void infoTarget(QJsonObject message);
    void deleteTarget(QJsonObject message);
    void deleteProbe(QJsonObject message);
    void probeReturn(QJsonObject message);
    void initialSyncBegin(QJsonObject message);
    void initialSyncEnd();

};

#endif // MONITOR_H
