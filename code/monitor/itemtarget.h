/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
#ifndef ITEMTARGET_H
#define ITEMTARGET_H
#include <QStandardItem>
#include <QMap>
#include <QString>
#include <QVariant>

class ItemTarget : public QStandardItem {
public:
    ItemTarget(QMap<QString, QVariant> info_target);
    QString name;
    QString orig_filter;
    int type() const;
    QMap<QString, QString> filter_hash;
    void updateInfo(QMap<QString, QVariant> info_target);
    void updateIconStatus();
    void updateProbeFilter(QString probe_name, QMap<QString, QVariant> obj);
    void deleteProbeFilter(QString probe_name);

private:
    QMap<QString, QVariant> target_properties;
    void updateFilter();
    void updateTooltip();
};

#endif // ITEMTARGET_H
