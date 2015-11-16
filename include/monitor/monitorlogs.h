#ifndef MONITORLOGS_H
#define MONITORLOGS_H

#include "include/nframecontainer.h"
#include "include/nframe.h"
#include "include/ngrid.h"
#include "include/ngridcontainer.h"
#include "include/monitor/monitor.h"
#include "include/network/supercastsignal.h"
#include "include/network/supercast.h"

#include <QWidget>
#include <QTabWidget>
#include <QIcon>
#include <QTextEdit>
#include <Qt>
#include <QByteArray>
#include <QList>
#include <QTableWidget>
#include <QHeaderView>
#include <QTableWidgetItem>
#include <QDateTime>
#include <QColor>
#include <QBrush>
#include <QVariant>
#include <QMap>

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
    void handleInitialSyncBegin(QVariant message);
    void handleHttpReply(QString body);
    void handleDbNotif(QVariant obj);

private:
    MonitorTableLogs* table;
};

#endif // MONITORLOGS_H
