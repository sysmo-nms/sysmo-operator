#ifndef TREEMODEL_H
#define TREEMODEL_H

#include "iostream"

#include "monitor.h"
#include "itemtarget.h"
#include "itemprobe.h"

#include <QObject>
#include <QWidget>
#include <QStandardItemModel>
#include <QStandardItem>
#include <QStringList>
#include <QJsonObject>
#include <QHash>
#include <QDebug>
#include <QList>
#include <QTimer>
#include <QModelIndex>

class TreeModel : public QStandardItemModel
{
    Q_OBJECT

public:
    explicit TreeModel(QWidget* parent = 0);
    ~TreeModel();

public slots:
    void handleInfoProbe(QJsonObject    message);
    void handleInfoTarget(QJsonObject   message);
    void handleDeleteProbe(QJsonObject  message);
    void handleDeleteTarget(QJsonObject message);
    void handleProbeReturn(QJsonObject  message);

private:
    QHash<QString, ItemTarget*>* targets = NULL;
    QHash<QString, ItemProbe*>*  probes  = NULL;

signals:
    void expandIndex(QModelIndex index);
};

#endif // TREEMODEL_H
