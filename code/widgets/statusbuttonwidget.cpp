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
#include "statusbuttonwidget.h"

#include <widgets/ngridcontainer.h>
#include <applications/monitor/monitor.h>

#include <QPixmap>
#include <QMap>
#include <QTimer>

/**
 * QFrame container for StatusButtons, handling sysmo monitor events
 * to set correct statuses on buttons.
 */
StatusButtonWidget::StatusButtonWidget(QWidget* parent) :
NFrameContainer(parent) {

    QTimer* timer = new QTimer(this);
    timer->setInterval(600);
    timer->setSingleShot(false);

    QObject::connect(
            Monitor::getInstance(), SIGNAL(deleteProbe(QVariant)),
            this, SLOT(handleDeleteProbe(QVariant)));
    QObject::connect(
            Monitor::getInstance(), SIGNAL(infoProbe(QVariant)),
            this, SLOT(handleInfoProbe(QVariant)));

    this->status_map = new QMap<QString, QString>();

    NGridContainer* grid = new NGridContainer();
    grid->setHorizontalSpacing(4);
    this->setLayout(grid);

    this->err = new StatusButton(this, "ERROR",
            QIcon(":/icons/weather-few-clouds-night"));
    this->warn = new StatusButton(this, "WARNING",
            QIcon(":/icons/weather-showers"));
    this->crit = new StatusButton(this, "CRITICAL",
            QIcon(":/icons/weather-severe-alert"));
    QObject::connect(
            timer, SIGNAL(timeout()),
            this->err, SLOT(toggleRed()));
    QObject::connect(
            timer, SIGNAL(timeout()),
            this->warn, SLOT(toggleRed()));
    QObject::connect(
            timer, SIGNAL(timeout()),
            this->crit, SLOT(toggleRed()));
    timer->start();

    grid->addWidget(this->crit, 0, 1);
    grid->addWidget(this->warn, 0, 2);
    grid->addWidget(this->err, 0, 3);
    //this->setFixedHeight(20);

}

void StatusButtonWidget::handleDeleteProbe(QVariant obj_var) {

    QMap<QString, QVariant> obj = obj_var.toMap();
    QString name = obj.value("name").toString();
    if (this->status_map->contains(name)) {
        QString status = this->status_map->take(name);
        this->decrementStatus(status);
    }

}

void StatusButtonWidget::handleInfoProbe(QVariant obj_var) {

    QMap<QString, QVariant> obj = obj_var.toMap();
    QString name = obj.value("name").toString();
    QString status = obj.value("status").toString();

    if (!this->status_map->contains(name)) {
        this->incrementStatus(status);
    } else {
        QString old_status = this->status_map->take(name);
        this->decrementStatus(old_status);
        this->incrementStatus(status);

    }
    this->status_map->insert(name, status);

}

void StatusButtonWidget::incrementStatus(QString status) {

    if (status == "ERROR")
        this->err->increment();
    else if (status == "WARNING")
        this->warn->increment();
    else if (status == "CRITICAL")
        this->crit->increment();

}

void StatusButtonWidget::decrementStatus(QString status) {

    if (status == "ERROR")
        this->err->decrement();
    else if (status == "WARNING")
        this->warn->decrement();
    else if (status == "CRITICAL")
        this->crit->decrement();

}
