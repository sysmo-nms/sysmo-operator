#ifndef ITEMTARGET_H
#define ITEMTARGET_H

#include "sysmo.h"

#include <QStandardItem>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonDocument>
#include <QVariant>
#include <QPixmap>
#include <QIcon>
#include <Qt>
#include <QString>
#include <QHash>
#include <QHashIterator>
#include <QStringList>
#include <QStringListIterator>

#include <QDebug>

class ItemTarget : public QStandardItem
{

public:
    ItemTarget(QJsonObject info_target);
    QString name;
    QString orig_filter;
    int type() const;
    QHash<QString, QString> filter_hash;
    void updateInfo(QJsonObject info_target);
    void updateIconStatus();
    void updateProbeFilter(QString probe_name, QJsonObject obj);
    void deleteProbeFilter(QString probe_name);

private:
    QJsonObject target_properties;
    void updateFilter();
    void updateTooltip();
};

#endif // ITEMTARGET_H
