#ifndef TREEVIEW_H
#define TREEVIEW_H

#include "monitor_tree/treemodel.h"
#include "monitor_tree/treedelegateprogress.h"

#include <QObject>
#include <QWidget>
#include <QAbstractItemView>
#include <Qt>
#include <QString>
#include <QSize>
#include <QTreeView>

class TreeView : public QTreeView
{
    Q_OBJECT

public:
    explicit TreeView(QWidget *parent = 0);
};

#endif // TREEVIEW_H
