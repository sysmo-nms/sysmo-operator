/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

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
#ifndef ITEMPROBE_H
#define ITEMPROBE_H

#include "sysmo.h"
#include "systemtray.h"
#include "qjson.h"

#include <QObject>
#include <QStandardItem>
#include <QList>
#include <QVariant>
#include <QIcon>
#include <Qt>
#include <QPixmap>
#include <QDateTime>
#include <QMap>

#include <QDebug>

class ItemProbe : public QStandardItem
{
public:
    ItemProbe(QMap<QString,QVariant> info_probe);
    QString name;
    QString belong_to;
    QStandardItem* item_status;
    QStandardItem* item_state;
    QStandardItem* item_progress;
    QStandardItem* item_last_return;
    QString orig_filter;
    QString targ_filter;
    int type() const;
    void updateInfo(QMap<QString,QVariant> info_probe);
    void updateReturnInfo(QMap<QString,QVariant> probe_return);
    void setTargetFilter(QString filter);

private:
    QPixmap icon;
    int status;
    void updateFilter();
};

#endif // ITEMPROBE_H
