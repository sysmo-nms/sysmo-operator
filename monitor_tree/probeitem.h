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
    QStandardItem* r1;
    QStandardItem* r2;
    QStandardItem* r3;
    QStandardItem* r4;
    QStandardItem* r5;
    int type() const;
    QVariant data(int role) const;

private:
    void updateInfo(QJsonObject info_probe);
    //QPixmap icon;
    QIcon icon;
};

#endif // PROBEITEM_H
