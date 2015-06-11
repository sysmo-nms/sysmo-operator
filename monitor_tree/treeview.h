#ifndef TREEVIEW_H
#define TREEVIEW_H

#include "delegateprobeprogress.h"
#include "treemodel.h"
#include "menuprobe.h"
#include "menutarget.h"
#include "monitor.h"
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
#include <QStandardItemModel>
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
    QStandardItemModel*    original_model;

public slots:
    void expandIndex(QModelIndex index);

private:
    QTimer* timer;
    MenuTarget* target_menu;
    MenuProbe*  probe_menu;

private slots:
    void openContextMenu(const QPoint point);
    void handleDoubleClicked(const QModelIndex index);
};

#endif // TREEVIEW_H
