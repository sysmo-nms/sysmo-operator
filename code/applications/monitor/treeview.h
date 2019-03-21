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
#ifndef TREEVIEW_H
#define TREEVIEW_H
#include <QTreeView>
#include <QWidget>
#include <QSortFilterProxyModel>
#include <QAction>
#include <QMenu>
#include <QModelIndex>
#include <QTimer>
#include <QPoint>

#include "treemodel.h"
#include "menuprobe.h"
#include "menutarget.h"

class TreeView : public QTreeView {
    Q_OBJECT

public:
    explicit TreeView(QWidget* parent = 0);
    ~TreeView();
    void stopTimer();

    QSortFilterProxyModel* filter_model;
    TreeModel* original_model;
    MenuTarget* target_menu;
    MenuProbe* probe_menu;
    QAction* add_target_action;
    QMenu* add_target_menu;

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
