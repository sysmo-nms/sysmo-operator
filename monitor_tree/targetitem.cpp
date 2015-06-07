#include "targetitem.h"

TargetItem::TargetItem(QJsonObject info_target) : QStandardItem()
{
    this->r1 = new TargetTypeItem();
    this->updateInfo(info_target);
}


void TargetItem::updateInfo(QJsonObject info_target)
{
    this->name              = info_target.value("name").toString("undefined");
    this->target_properties = info_target.value("properties").toObject();
    QString hostname = this->target_properties.value("host").toString("undefined");
    QString type     = this->target_properties.value("type").toString("undefined");

    /* set r1 "Type/Hostname" */
    if (type == "router") {
        this->r1->icon = QPixmap(":/pixmaps/router.png");
    } else if (type == "switch") {
        this->r1->icon = QPixmap(":/pixmaps/hub.png");
    } else if (type == "wireless") {
        this->r1->icon = QPixmap(":/pixmaps/wireless-router.png");
    } else if (type == "server") {
        this->r1->icon = QPixmap(":/pixmaps/server-generic.png");
    } else if (type == "printer") {
        this->r1->icon = QPixmap(":/pixmaps/printer.png");
    } else {
        this->r1->icon = QPixmap();
    }
    this->r1->text_variable = type.append(" ").append(hostname);

    this->icon = QPixmap(":/pixmaps/weather-clear.png");
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
