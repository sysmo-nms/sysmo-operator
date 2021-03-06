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
#include "treeview.h"

#include "windows/probewindow.h"
#include "sysmo.h"
#include "actions/monitoractions.h"
#include "delegateprobeprogress.h"
#include "monitorwidget.h"
#include <QHeaderView>
#include <QObject>
#include <QAbstractItemView>
#include <Qt>
#include <QString>
#include <QSize>
#include <QModelIndex>
#include <QFile>
#include <QIODevice>
#include <QStandardItem>
#include <QSettings>

#include <QDebug>

TreeView* TreeView::singleton = NULL;

TreeView::TreeView(QWidget* parent) : QTreeView(parent) {

    // empty treeview right clic
    this->add_target_action = new QAction("Create a new target...", this);
    this->add_target_action->setIcon(QIcon(":/icons/list-add.png"));
    this->add_target_menu = new QMenu(this);
    this->add_target_menu->addAction(this->add_target_action);

    TreeView::singleton = this;
    this->target_menu = new MenuTarget(this);
    this->probe_menu = new MenuProbe(this);
    QObject::connect(
            this, SIGNAL(doubleClicked(QModelIndex)),
            this, SLOT(handleDoubleClicked(QModelIndex)));
    this->setItemsExpandable(true);
    this->setRootIsDecorated(false);
    this->setWordWrap(true);
    this->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
    this->setSelectionMode(QAbstractItemView::SingleSelection);
    this->setEditTriggers(QAbstractItemView::NoEditTriggers);
    this->setContextMenuPolicy(Qt::CustomContextMenu);
    QObject::connect(
            this, SIGNAL(customContextMenuRequested(QPoint)),
            this, SLOT(openContextMenu(QPoint)));
    this->setObjectName("MonitorTreeView");
    this->setIconSize(QSize(22, 22));
    this->setAnimated(true);
    this->setAlternatingRowColors(true);
    this->setAllColumnsShowFocus(false);
    this->setSortingEnabled(true);
    this->setExpandsOnDoubleClick(false);

    this->original_model = new TreeModel(this);
    this->filter_model = new QSortFilterProxyModel(this);
    this->filter_model->setSourceModel(this->original_model);
    this->filter_model->setDynamicSortFilter(true);
    this->filter_model->setFilterCaseSensitivity(Qt::CaseInsensitive);
    this->filter_model->setFilterRole(Sysmo::ROLE_FILTER_STRING);

    this->timer = new QTimer(this);
    this->timer->setInterval(1000);
    this->timer->setSingleShot(false);
    this->timer->start();
    DelegateProbeProgress* progress = new DelegateProbeProgress(this);

    QObject::connect(
            this->original_model, SIGNAL(expandIndex(QModelIndex)),
            this, SLOT(expandIndex(QModelIndex)));

    QObject::connect(
            this->original_model, SIGNAL(selectIndex(QModelIndex)),
            this, SLOT(selectIndex(QModelIndex)));
    /*
     * connect delegate first
     */
    QObject::connect(
            this->timer, SIGNAL(timeout()),
            progress, SLOT(ticTimeout()));

    QObject::connect(
            this->timer, SIGNAL(timeout()),
            this->viewport(), SLOT(update()));

    this->setItemDelegateForColumn(3, progress);

    /*
     * Set stylesheet mainly for custom branch draw
     */
    QFile file(":/tree/tree.qss");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    this->setStyleSheet(file.readAll());
    file.close();

    /*
     * Acceptable defaults. Overriden by restore state.
     */
    this->setColumnWidth(0, 250);
    this->setColumnWidth(1, 65);
    this->setColumnWidth(2, 65);
    this->setColumnWidth(3, 100);

    /*
     * Then wait for initialSyncEnd() slot to be triggered and
     * finalize the initialisation.
     */

}

void TreeView::initialSyncEnd() {

    this->restoreStateFromSettings();
    this->setModel(this->filter_model);
    this->expandAll();
    this->update();

}

TreeView::~TreeView() {

    QSettings s;
    s.setValue("treeview/header_state", this->header()->saveState());
    s.setValue("treeview/header_geometry", this->header()->saveGeometry());

}

void TreeView::restoreStateFromSettings() {

    QSettings s;
    QVariant hs = s.value("treeview/header_state");
    if (hs.isValid()) {
        this->header()->restoreState(hs.toByteArray());
    }
    QVariant hg = s.value("treeview/header_geometry");
    if (hg.isValid()) {
        this->header()->restoreGeometry(hg.toByteArray());
    }

}


// SLOTS

void TreeView::expandIndex(QModelIndex index) {

    this->expand(this->filter_model->mapFromSource(index));

}

void TreeView::selectIndex(QModelIndex index) {

    this->setCurrentIndex(this->filter_model->mapFromSource(index));

}

void TreeView::stopTimer() {
    this->timer->stop();
}

void TreeView::openContextMenu(const QPoint point) {

    QModelIndex index = this->filter_model->mapToSource(this->indexAt(point));
    if (!index.isValid()) {
        QPoint at = this->mapToGlobal(point);
        at.setX(at.x() + 12);
        this->add_target_menu->popup(at);
        return;
    }

    QModelIndex element = index.sibling(index.row(), 0);
    QStandardItem* item = this->original_model->itemFromIndex(element);

    if (item->type() == Sysmo::TYPE_PROBE) {
        QString probe = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
        this->probe_menu->showMenuFor(probe, this->mapToGlobal(point));
    } else if (item->type() == Sysmo::TYPE_TARGET) {
        QString target = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
        this->target_menu->showMenuFor(target, this->mapToGlobal(point));
    }

}

void TreeView::handleDoubleClicked(const QModelIndex index) {

    QModelIndex idx_sibling = index.sibling(index.row(), 0);
    QModelIndex idx_origin = this->filter_model->mapToSource(idx_sibling);
    QStandardItem* item = this->original_model->itemFromIndex(idx_origin);

    QString name = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
    if (item->type() == Sysmo::TYPE_PROBE) {
        ProbeWindow::openWindow(name);
    } else if (item->type() == Sysmo::TYPE_TARGET) {
        MonitorActions::openActionFor(name);
    }

}
