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
#include "itemtarget.h"
#include "targetutils.h"

#include <sysmo.h>
#include <network/qjson.h>

#include <QPixmap>
#include <QIcon>
#include <Qt>
#include <QMapIterator>
#include <QStringList>
#include <QStringListIterator>

#include <QDebug>

int ItemTarget::type() const {
    return Sysmo::TYPE_TARGET;
}

ItemTarget::ItemTarget(QMap<QString, QVariant> info_target) : QStandardItem() {

    this->updateInfo(info_target);
    this->updateIconStatus();

}

void ItemTarget::updateProbeFilter(QString probe_name, QMap<QString, QVariant> obj) {

    this->filter_hash.insert(probe_name, QJson::encode(obj));
    this->updateFilter();

}

void ItemTarget::deleteProbeFilter(QString probe_name) {

    this->filter_hash.remove(probe_name);
    this->updateFilter();

}

void ItemTarget::updateFilter() {

    QString str = this->orig_filter;
    QMapIterator<QString, QString> i(this->filter_hash);
    while (i.hasNext()) {
        i.next();
        str = str + i.value();
    }
    this->setData(str.remove("\""), Sysmo::ROLE_FILTER_STRING);

}

void ItemTarget::updateInfo(QMap<QString, QVariant> info_target) {

    this->name = info_target.value("name").toString();
    this->target_properties = info_target.value("properties").toMap();

    this->setData(this->name, Sysmo::ROLE_ELEMENT_NAME);

    QString display = TargetUtils::getName(this->target_properties);

    this->setData(display, Qt::DisplayRole);

    this->orig_filter = QJson::encode(info_target);
    this->setData(this->orig_filter, Sysmo::ROLE_FILTER_ORIG);
    this->updateFilter();
    this->updateTooltip();

}

void ItemTarget::updateTooltip() {

    QString tooltip;
    QStringList keys = this->target_properties.keys();
    keys.sort();
    QStringListIterator it(keys);
    tooltip += "<table>";
    while (it.hasNext()) {
        QString key = it.next();
        QString val = this->target_properties.value(key).toString();
        tooltip += "<tr><td><b>" + key + "</b></td><td>: " + val + "</td></tr>";
    }
    tooltip += "</table>";
    this->setToolTip(tooltip);

}

void ItemTarget::updateIconStatus() {

    int status = 0;
    if (this->rowCount() == 0) {
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"), Qt::DecorationRole);
        return;
    }

    for (int i = 0; i < this->rowCount(); i++) {
        int pstatus = this->child(i, 0)->data(Sysmo::ROLE_PROBE_STATUS)
                .toInt(NULL);
        if (pstatus > status) {
            status = pstatus;
        }
    }
    if (status == Sysmo::STATUS_OK) {
        this->setData(QPixmap(":/pixmaps/weather-clear.png"), Qt::DecorationRole);
    } else if (status == Sysmo::STATUS_UNKNOWN) {
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"), Qt::DecorationRole);
    } else if (status == Sysmo::STATUS_ERROR) {
        this->setData(QPixmap(":/pixmaps/weather-few-clouds-night.png"), Qt::DecorationRole);
    } else if (status == Sysmo::STATUS_WARNING) {
        this->setData(QPixmap(":/pixmaps/weather-showers.png"), Qt::DecorationRole);
    } else if (status == Sysmo::STATUS_CRITICAL) {
        this->setData(QPixmap(":/pixmaps/weather-severe-alert.png"), Qt::DecorationRole);
    }

}

