#ifndef MONITORCHANNEL_H
#define MONITORCHANNEL_H

#include <QJsonObject>
#include <QDebug>

class MonitorChannel
{
public:
    MonitorChannel(QString probe_name);
    ~MonitorChannel();

public slots:
    virtual void handleEvent(QJsonObject event) = 0;

};

#endif // MONITORCHANNEL_H
