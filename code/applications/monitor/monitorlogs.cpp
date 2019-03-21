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
#include "monitorlogs.h"
#include "monitor.h"


#include <widgets/nframecontainer.h>
#include <widgets/nframe.h>
#include <widgets/ngrid.h>
#include <widgets/ngridcontainer.h>
#include <network/supercastsignal.h>
#include <network/supercast.h>
#include <network/qjson.h>

#include <QIcon>
#include <QTextEdit>
#include <Qt>
#include <QByteArray>
#include <QList>
#include <QHeaderView>
#include <QDateTime>
#include <QBrush>
#include <QMap>

#include <QDebug>

MonitorLogs::MonitorLogs(QWidget* parent) : QTabWidget(parent) {

    this->table = new MonitorTableLogs(this);
    this->table->setColumnCount(5);
    this->table->verticalHeader()->hide();
    QStringList headers;
    headers << "Date" << "Target" << "Probe" << "Status" << "Message";
    this->table->setHorizontalHeaderLabels(headers);
    QHeaderView* head = this->table->horizontalHeader();
    head->setStretchLastSection(true);
    NFrameContainer* f1 = new NFrameContainer(this);
    NGrid* g1 = new NGrid();
    f1->setLayout(g1);
    g1->addWidget(this->table);
    NFrame* f2 = new NFrame(this);

    this->insertTab(0, f1, QIcon(":/icons/edit-paste.png"), "Table logs");
    this->insertTab(1, f2, QIcon(":/icons/appointment-new.png"), "Timeline logs");
    this->setTabEnabled(1, false);
    QObject::connect(
            Monitor::getInstance(), SIGNAL(initialSyncBegin(QVariant)),
            this, SLOT(handleInitialSyncBegin(QVariant)));
    QObject::connect(
            Monitor::getInstance(), SIGNAL(dbNotification(QVariant)),
            this, SLOT(handleDbNotif(QVariant)));

}

void MonitorLogs::handleInitialSyncBegin(QVariant message_var) {

    QMap<QString, QVariant> message = message_var.toMap();
    QString syncDir = "sync";
    QString dumpDir = message.value("dumpDir").toString();
    QString evtFile = message.value("latestEventsFile").toString();
    QString http_tmp = "/%1/%2/%3";
    QString http_url = http_tmp.arg(syncDir).arg(dumpDir).arg(evtFile);
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
            sig, SIGNAL(serverMessage(QString)),
            this, SLOT(handleHttpReply(QString)));
    Supercast::httpGet(http_url, sig);

}

void MonitorLogs::handleHttpReply(QString body) {

    QVariant json_var = QJson::decode(body);
    QList<QVariant> json_array = json_var.toList();
    this->table->setRowCount(json_array.size());

    int j = 0;
    for (int i = 0; i < json_array.size(); i++) {
        QMap<QString, QVariant> obj = json_array.at(i).toMap();
        int timestamp = obj.value("DATE_CREATED").toInt();
        QDateTime date = QDateTime::fromTime_t(timestamp);
        CustomTableItem* created = new CustomTableItem(date.toString("yyyy-MM-d hh:mm:ss"));
        CustomTableItem* target = new CustomTableItem(obj.value("HOST_DISPLAY").toString());
        CustomTableItem* probe = new CustomTableItem(obj.value("PROBE_DISPLAY").toString());
        StatusTableItem* status = new StatusTableItem(obj.value("STATUS").toString());
        CustomTableItem* message = new CustomTableItem(obj.value("RETURN_STRING").toString());
        this->table->setItem(j, 0, created);
        this->table->setItem(j, 1, target);
        this->table->setItem(j, 2, probe);
        this->table->setItem(j, 3, status);
        this->table->setItem(j, 4, message);
        this->table->setRowHeight(j, 20);
        j++;
        qDebug() << obj;
    }

}

void MonitorLogs::handleDbNotif(QVariant obj_var) {

    QMap<QString, QVariant> obj = obj_var.toMap();
    int timestamp = obj.value("DATE_CREATED").toInt();
    QDateTime date = QDateTime::fromTime_t(timestamp);
    CustomTableItem* created = new CustomTableItem(date.toString("yyyy-MM-d hh:mm:ss"));
    CustomTableItem* target = new CustomTableItem(obj.value("HOST_DISPLAY").toString());
    CustomTableItem* probe = new CustomTableItem(obj.value("PROBE_DISPLAY").toString());
    StatusTableItem* status = new StatusTableItem(obj.value("STATUS").toString());
    CustomTableItem* message = new CustomTableItem(obj.value("RETURN_STRING").toString());

    this->table->insertRow(0);
    this->table->setItem(0, 0, created);
    this->table->setItem(0, 1, target);
    this->table->setItem(0, 2, probe);
    this->table->setItem(0, 3, status);
    this->table->setItem(0, 4, message);
    this->table->setRowHeight(0, 20);

    qDebug() << "have received: " << message;

}

MonitorTableLogs::MonitorTableLogs(QWidget *parent) : QTableWidget(parent) {
}

CustomTableItem::CustomTableItem(QString text) : QTableWidgetItem(text) {

    this->setFlags(Qt::ItemIsEnabled);

}


QColor StatusTableItem::red = QColor(239, 41, 41);
QColor StatusTableItem::yellow = QColor(237, 212, 0);
QColor StatusTableItem::green = QColor(237, 212, 0);
QColor StatusTableItem::white = QColor(254, 254, 254);
QColor StatusTableItem::dark = QColor(40, 40, 40);

StatusTableItem::StatusTableItem(QString text) : CustomTableItem(text) {
    if (text == "CRITICAL") {
        this->setBackground(QBrush(StatusTableItem::red));
        this->setForeground(QBrush(StatusTableItem::white));
    } else if (text == "WARNING") {
        this->setBackground(QBrush(StatusTableItem::yellow));
    } else if (text == "ERROR") {
        this->setBackground(QBrush(StatusTableItem::dark));
        this->setForeground(QBrush(StatusTableItem::white));
    }

}
