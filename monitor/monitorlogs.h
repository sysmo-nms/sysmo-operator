#ifndef MONITORLOGS_H
#define MONITORLOGS_H

#include "nframecontainer.h"
#include "nframe.h"
#include "ngrid.h"
#include "ngridcontainer.h"
#include "monitor/monitor.h"
#include "network/supercastsignal.h"
#include "network/supercast.h"

#include <QWidget>
#include <QTabWidget>
#include <QIcon>
#include <QTextEdit>
#include <QJsonObject>
#include <Qt>
#include <QJsonDocument>
#include <QJsonArray>
#include <QByteArray>
#include <QList>
#include <QTableWidget>
#include <QHeaderView>
#include <QTableWidgetItem>
#include <QDateTime>

#include <QDebug>

class MonitorTableLogs : public QTableWidget
{

public:
    explicit MonitorTableLogs(QWidget* parent = 0);
};


class MonitorLogs : public QTabWidget
{
    Q_OBJECT
public:
    explicit MonitorLogs(QWidget* parent = 0);

public slots:
    void handleInitialSyncBegin(QJsonObject message);
    void handleHttpReply(QString body);

private:
    MonitorTableLogs* table;
};

#endif // MONITORLOGS_H
