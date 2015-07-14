#ifndef MONITORPROXYWIDGET_H
#define MONITORPROXYWIDGET_H

#include "monitor/monitorchannel.h"
#include "monitor/monitor.h"

#include <QObject>
#include <QWidget>
#include <QJsonObject>
#include <QDebug>

class MonitorProxyWidget : public QWidget
{
    Q_OBJECT
public:
    explicit MonitorProxyWidget(QWidget *parent = 0);
    ~MonitorProxyWidget();
    void connectChan(QString channel);

public slots:
    virtual void handleEvent(QJsonObject event) = 0;
};

#endif // MONITORPROXYWIDGET_H
