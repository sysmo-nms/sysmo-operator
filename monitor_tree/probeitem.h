#ifndef PROBEITEM_H
#define PROBEITEM_H

#include "progressitem.h"

#include <QObject>
#include <QJsonObject>
#include <QStandardItem>
#include <QList>
#include <QVariant>
#include <QIcon>
#include <Qt>
#include <QDebug>
#include <QPixmap>

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
    QVariant data(int role) const;

private:
    void updateInfo(QJsonObject info_probe);
    QPixmap icon;
};

#endif // PROBEITEM_H
