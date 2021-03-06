/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef MONITORLOGS_H
#define MONITORLOGS_H
#include <QTableWidget>
#include <QString>
#include <QColor>
#include <QTableWidgetItem>
#include <QWidget>
#include <QTabWidget>
#include <QVariant>

class CustomTableItem : public QTableWidgetItem {
public:
    explicit CustomTableItem(QString text);
};

class StatusTableItem : public CustomTableItem {
public:
    explicit StatusTableItem(QString text);

private:
    static QColor red;
    static QColor yellow;
    static QColor green;
    static QColor white;
    static QColor dark;
};

class MonitorTableLogs : public QTableWidget {
public:
    explicit MonitorTableLogs(QWidget* parent = 0);
};

class MonitorLogs : public QTabWidget {
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
