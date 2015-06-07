#ifndef TARGETITEM_H
#define TARGETITEM_H

#include "iostream"

#include <QStandardItem>
#include <QJsonObject>
#include <QVariant>
#include <QDebug>
#include <QPixmap>
#include <QIcon>
#include <Qt>
#include <QDebug>

class TargetItem : public QStandardItem
{

public:
    TargetItem(QJsonObject info_target);
    QString name;
    QStandardItem* r1 = NULL;
    QVariant data(int role) const;
    int type() const;

private:
    void updateInfo(QJsonObject info_target);
    QJsonObject target_properties;
    QPixmap icon;
    //QIcon icon;
};

#endif // TARGETITEM_H
