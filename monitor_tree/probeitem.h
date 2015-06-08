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
    QStandardItem* r1 = NULL;
    QStandardItem* r2 = NULL;
    QStandardItem* r3 = NULL;
    QStandardItem* r4 = NULL;
    QStandardItem* r5 = NULL;
    int type() const;
    void updateInfo(QJsonObject  info_probe);
    void updateReturnInfo(QJsonObject probe_return);

private:
    QPixmap icon;
    int status;
};

#endif // PROBEITEM_H
