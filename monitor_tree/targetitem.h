#ifndef TARGETITEM_H
#define TARGETITEM_H

#include "iostream"

#include "targettypeitem.h"
#include "sysmo.h"

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
    TargetTypeItem* r1 = NULL;
    QVariant data(int role) const;
    int type() const;
    void updateInfo(QJsonObject info_target);
    void updateIconStatus();

private:
    QJsonObject target_properties;
    QPixmap icon;
};

#endif // TARGETITEM_H
