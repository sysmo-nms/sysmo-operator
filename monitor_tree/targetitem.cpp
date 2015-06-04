#include "targetitem.h"

TargetItem::TargetItem(QJsonObject info_target) : QStandardItem()
{
    this->name = info_target.value("name").toString("undefined");
    this->setText(this->name);
    this->updateInfo(info_target);
    //this->icon = QPixmap(":/ressources/images/32/dialog-information.png");
    this->icon = QIcon(":/ressources/images/32/dialog-information.png");
    //qDebug() << this->icon.cacheKey();
}


void TargetItem::updateInfo(QJsonObject info_target)
{
    this->target_properties = info_target.value("properties").toObject();
    QString hostname = this->target_properties.value("host").toString("undefined");
    this->r1 = new QStandardItem(hostname);
}

QVariant TargetItem::data(int role) const
{
    if (role == Qt::DecorationRole) {return this->icon;}
    if (role == Qt::DisplayRole)    {return this->name;}
    return QStandardItem::data(role);
}

int TargetItem::type() const
{
    return 1000;
}
