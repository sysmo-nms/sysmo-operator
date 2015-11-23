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
#ifndef TREEMODEL_H
#define TREEMODEL_H

#include "include/monitor/monitor.h"
#include "include/monitor/itemtarget.h"
#include "include/monitor/itemprobe.h"

#include <QObject>
#include <QWidget>
#include <QStandardItemModel>
#include <QStandardItem>
#include <QStringList>
#include <QMap>
#include <QList>
#include <QTimer>
#include <QModelIndex>
#include <QTreeView>
#include <QVariant>

#include <QDebug>

class TreeModel : public QStandardItemModel
{
    Q_OBJECT

public:
    explicit TreeModel(QWidget* parent = 0);
    ~TreeModel();

public slots:
    void handleInfoProbe(QVariant message);
    void handleInfoTarget(QVariant message);
    void handleDeleteProbe(QVariant message);
    void handleDeleteTarget(QVariant message);
    void handleProbeReturn(QVariant message);

private:
    QMap<QString, ItemTarget*>* targets;
    QMap<QString, ItemProbe*>*  probes;

signals:
    void expandIndex(QModelIndex index);
    void selectIndex(QModelIndex index);
};

#endif // TREEMODEL_H
