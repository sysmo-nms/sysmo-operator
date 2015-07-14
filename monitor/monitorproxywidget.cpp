#include "monitorproxywidget.h"

MonitorProxyWidget::MonitorProxyWidget(QWidget *parent) : QWidget(parent)
{
    qDebug() << "init chann proxy";
}

void MonitorProxyWidget::connectChan(QString channel) {
    MonitorChannel* chan = Monitor::getChannel(channel);
    qDebug() << "get channel";
}

MonitorProxyWidget::~MonitorProxyWidget()
{
    qDebug() << "close chann proxy";
}
