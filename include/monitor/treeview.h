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
#ifndef TREEVIEW_H
#define TREEVIEW_H

#include "include/monitor/delegateprobeprogress.h"
#include "include/actions/monitoractions.h"
#include "include/monitor/treemodel.h"
#include "include/monitor/menuprobe.h"
#include "include/monitor/menutarget.h"
#include "include/monitor/monitorwidget.h"
#include "include/windows/probewindow.h"
#include "include/sysmo.h"

#include <QObject>
#include <QWidget>
#include <QAbstractItemView>
#include <Qt>
#include <QString>
#include <QSize>
#include <QTreeView>
#include <QTimer>
#include <QSortFilterProxyModel>
#include <QModelIndex>
#include <QFile>
#include <QIODevice>
#include <QPoint>
#include <QStandardItem>
#include <QModelIndex>
#include <QSettings>

#include <QDebug>

class TreeView : public QTreeView
{
    Q_OBJECT

public:
    explicit TreeView(QWidget* parent = 0);
    ~TreeView();
    void stopTimer();

    QSortFilterProxyModel* filter_model;
    TreeModel*             original_model;
    MenuTarget*            target_menu;
    MenuProbe*             probe_menu;
    QAction*               add_target_action;
    QMenu*                 add_target_menu;

public slots:
    void expandIndex(QModelIndex index);
    void selectIndex(QModelIndex index);
    void initialSyncEnd();

private:
    QTimer* timer;
    static TreeView* singleton;
    void restoreStateFromSettings();

private slots:
    void openContextMenu(const QPoint point);
    void handleDoubleClicked(const QModelIndex index);
};

#endif // TREEVIEW_H
