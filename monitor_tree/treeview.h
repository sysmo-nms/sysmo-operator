#ifndef TREEVIEW_H
#define TREEVIEW_H

#include "treedelegateprogress.h"
#include "treemodel.h"

#include <QObject>
#include <QWidget>
#include <QAbstractItemView>
#include <Qt>
#include <QString>
#include <QSize>
#include <QTreeView>
#include <QTimer>

class TreeView : public QTreeView
{
    Q_OBJECT

public:
    explicit TreeView(QWidget* parent = 0);
    ~TreeView();
    void stopTimer();

private:
    QTimer* timer;
};

#endif // TREEVIEW_H
