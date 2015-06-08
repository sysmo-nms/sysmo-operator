#ifndef TARGETITEM_H
#define TARGETITEM_H

#include "iostream"

#include "sysmo.h"

#include <QStandardItem>
#include <QJsonObject>
#include <QVariant>
#include <QDebug>
#include <QPixmap>
#include <QIcon>
#include <Qt>
#include <QDebug>
#include <QString>

class TargetItem : public QStandardItem
{

public:
    TargetItem(QJsonObject info_target);
    QString name;
    QStandardItem* r1 = NULL;
    int type() const;
    void updateInfo(QJsonObject info_target);
    void updateIconStatus();

private:
    QJsonObject target_properties;
};

#endif // TARGETITEM_H
