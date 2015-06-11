#ifndef TREEVIEW_H
#define TREEVIEW_H

#include "delegateprobeprogress.h"
#include "treemodel.h"
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

class TreeView : public QTreeView
{
    Q_OBJECT

public:
    explicit TreeView(QWidget* parent = 0);
    ~TreeView();
    void stopTimer();
    QSortFilterProxyModel* filter_model;

public slots:
    void expandIndex(QModelIndex index);

private:
    QTimer* timer;
};

#endif // TREEVIEW_H
