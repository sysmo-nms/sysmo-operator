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
