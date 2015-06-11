#ifndef ITEMTARGET_H
#define ITEMTARGET_H

#include "iostream"

#include "sysmo.h"

#include <QStandardItem>
#include <QJsonObject>
#include <QJsonValue>
#include <QVariant>
#include <QDebug>
#include <QPixmap>
#include <QIcon>
#include <Qt>
#include <QDebug>
#include <QString>

class ItemTarget : public QStandardItem
{

public:
    ItemTarget(QJsonObject info_target);
    QString name;
    int type() const;
    void updateInfo(QJsonObject info_target);
    void updateIconStatus();

private:
    QJsonObject target_properties;
};

#endif // ITEMTARGET_H
