#ifndef ITEMPROBE_H
#define ITEMPROBE_H

#include "sysmo.h"
#include "systemtray.h"

#include <QObject>
#include <QJsonObject>
#include <QJsonDocument>
#include <QStandardItem>
#include <QList>
#include <QVariant>
#include <QIcon>
#include <Qt>
#include <QPixmap>
#include <QDateTime>

#include <QDebug>

class ItemProbe : public QStandardItem
{
public:
    ItemProbe(QJsonObject info_probe);
    QString name;
    QString belong_to;
    QStandardItem* item_status      = NULL;
    QStandardItem* item_state       = NULL;
    QStandardItem* item_progress    = NULL;
    QStandardItem* item_last_return = NULL;
    QString orig_filter = "";
    QString targ_filter = "";
    int type() const;
    void updateInfo(QJsonObject  info_probe);
    void updateReturnInfo(QJsonObject probe_return);
    void setTargetFilter(QString filter);

private:
    QPixmap icon;
    int status;
    void updateFilter();
};

#endif // ITEMPROBE_H
