#ifndef TREEMODEL_H
#define TREEMODEL_H

#include <QObject>
#include <QWidget>
#include <QStandardItemModel>
#include <QStringList>

class TreeModel : public QStandardItemModel
{
    Q_OBJECT

public:
    TreeModel(QWidget *parent = 0);
};

#endif // TREEMODEL_H
