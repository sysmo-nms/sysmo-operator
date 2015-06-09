#include "targetitem.h"

int TargetItem::type() const { return Sysmo::TYPE_TARGET; }

TargetItem::TargetItem(QJsonObject info_target) : QStandardItem()
{
    this->r1 = new QStandardItem();
    this->updateInfo(info_target);
    this->setData("undefined", Qt::DisplayRole);
    this->setData(QPixmap(":/pixmaps/weather-clear.png"), Qt::DecorationRole);
}


void TargetItem::updateInfo(QJsonObject info_target)
{
    this->name              = info_target.value("name").toString("undefined");
    this->target_properties = info_target.value("properties").toObject();
    QString hostname = this->target_properties.value("host").toString("undefined");
    QString type     = this->target_properties.value("type").toString("undefined");

    /*
     * set r1 "Type/Hostname"
     */
    if (type == "router")
        this->r1->setData(QPixmap(":/pixmaps/router.png"), Qt::DecorationRole);

    else if (type == "switch")
        this->r1->setData(QPixmap(":/pixmaps/hub.png"), Qt::DecorationRole);

    else if (type == "wireless")
        this->r1->setData(QPixmap(":/pixmaps/wireless-router.png"), Qt::DecorationRole);

    else if (type == "server")
        this->r1->setData(QPixmap(":/pixmaps/server-generic.png"), Qt::DecorationRole);

    else if (type == "printer")
        this->r1->setData(QPixmap(":/pixmaps/printer.png"), Qt::DecorationRole);

    else
        this->r1->setData(QPixmap(), Qt::DecorationRole);

    this->r1->setData(type.append(" ").append(hostname), Qt::DisplayRole);

    this->setData("world", Sysmo::ROLE_FILTER_STRING);

}


void TargetItem::updateIconStatus()
{

    int status = 0;
    for (int i = 0; i < this->rowCount(); i ++)
    {
        int pstatus = this->child(i, 0)->data(Sysmo::ROLE_PROBE_STATUS)
                                                     .toInt(NULL);
        if (pstatus > status) {status = pstatus;}
    }
    if (status == Sysmo::STATUS_OK)
        this->setData(QPixmap(":/pixmaps/weather-clear.png"), Qt::DecorationRole);

    else if (status == Sysmo::STATUS_UNKNOWN)
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"), Qt::DecorationRole);

    else if (status == Sysmo::STATUS_ERROR)
        this->setData(QPixmap(":/pixmaps/weather-few-clouds-night.png"), Qt::DecorationRole);

    else if (status == Sysmo::STATUS_WARNING)
        this->setData(QPixmap(":/pixmaps/weather-showers.png"), Qt::DecorationRole);

    else if (status == Sysmo::STATUS_CRITICAL)
        this->setData(QPixmap(":/pixmaps/weather-severe-alert.png"), Qt::DecorationRole);
}


