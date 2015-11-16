#ifndef ITEMTARGET_H
#define ITEMTARGET_H

#include "include/sysmo.h"
#include "include/qjson.h"

#include <QStandardItem>
#include <QVariant>
#include <QPixmap>
#include <QIcon>
#include <Qt>
#include <QString>
#include <QMap>
#include <QMapIterator>
#include <QStringList>
#include <QStringListIterator>

#include <QDebug>

class ItemTarget : public QStandardItem
{

public:
    ItemTarget(QMap<QString,QVariant> info_target);
    QString name;
    QString orig_filter;
    int type() const;
    QMap<QString, QString> filter_hash;
    void updateInfo(QMap<QString,QVariant> info_target);
    void updateIconStatus();
    void updateProbeFilter(QString probe_name, QMap<QString,QVariant> obj);
    void deleteProbeFilter(QString probe_name);

private:
    QMap<QString,QVariant> target_properties;
    void updateFilter();
    void updateTooltip();
};

#endif // ITEMTARGET_H
