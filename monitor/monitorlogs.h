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
#include <QColor>
#include <QBrush>

#include <QDebug>

class CustomTableItem : public QTableWidgetItem
{
public:
    explicit CustomTableItem(QString text);
};

class StatusTableItem : public CustomTableItem
{
public:
    explicit StatusTableItem(QString text);

private:
    static QColor red;
    static QColor yellow;
    static QColor green;
    static QColor white;
    static QColor dark;
};

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
    void handleDbNotif(QJsonObject obj);

private:
    MonitorTableLogs* table;
};

#endif // MONITORLOGS_H
