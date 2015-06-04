#ifndef TARGETITEM_H
#define TARGETITEM_H

#include "iostream"

#include <QStandardItem>
#include <QJsonObject>
#include <QVariant>
#include <QDebug>
#include <QPixmap>
#include <Qt>

class TargetItem : public QStandardItem
{

public:
    TargetItem(QJsonObject info_target);
    QString name;
    QStandardItem* r1;
    QVariant data(int role) const;
    int type() const;

private:
    void updateInfo(QJsonObject info_target);
    QJsonObject target_properties;
    QIcon icon;
};

#endif // TARGETITEM_H
