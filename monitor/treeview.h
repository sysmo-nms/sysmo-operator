#ifndef TREEVIEW_H
#define TREEVIEW_H

#include "monitor/delegateprobeprogress.h"
#include "actions/monitoractions.h"
#include "monitor/treemodel.h"
#include "monitor/menuprobe.h"
#include "monitor/menutarget.h"
#include "monitor/monitorwidget.h"
#include "windows/probewindow.h"
#include "sysmo.h"

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

public slots:
    void expandIndex(QModelIndex index);
    void selectIndex(QModelIndex index);

private:
    QTimer* timer;
    static TreeView* singleton;

private slots:
    void openContextMenu(const QPoint point);
    void handleDoubleClicked(const QModelIndex index);
};

#endif // TREEVIEW_H
