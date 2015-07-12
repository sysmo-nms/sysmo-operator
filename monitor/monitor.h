#ifndef MONITOR_H
#define MONITOR_H

#include "network/supercast.h"
#include "monitor/monitorchannel.h"

#include <QObject>
#include <QHash>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QString>

#include <QDebug>

class Monitor : public QObject
{
    Q_OBJECT
public:
    explicit Monitor(QObject *parent = 0);
    ~Monitor();
    static Monitor* getInstance();
    QHash<QString, QJsonObject>* targets = NULL;
    QHash<QString, QJsonObject>* probes  = NULL;

private:
    static Monitor* singleton;

public slots:
    void handleServerMessage(QJsonObject message);

signals:
    void infoProbe(    QJsonObject message);
    void infoTarget(   QJsonObject message);
    void deleteTarget( QJsonObject message);
    void deleteProbe(  QJsonObject message);
    void probeReturn(  QJsonObject message);

};

#endif // MONITOR_H
