#ifndef PROBEITEM_H
#define PROBEITEM_H

#include "sysmo.h"

#include <QObject>
#include <QJsonObject>
#include <QStandardItem>
#include <QList>
#include <QVariant>
#include <QIcon>
#include <Qt>
#include <QDebug>
#include <QPixmap>
#include <QDateTime>

class ProbeItem : public QStandardItem
{
public:
    ProbeItem(QJsonObject info_probe);
    QString name;
    QString belong_to;
    QStandardItem* item_status      = NULL;
    QStandardItem* item_state       = NULL;
    QStandardItem* item_progress    = NULL;
    QStandardItem* item_last_return = NULL;
    int type() const;
    void updateInfo(QJsonObject  info_probe);
    void updateReturnInfo(QJsonObject probe_return);

private:
    QPixmap icon;
    int status;
};

#endif // PROBEITEM_H
