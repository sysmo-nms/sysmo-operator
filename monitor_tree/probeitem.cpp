#include "probeitem.h"

ProbeItem::ProbeItem(QJsonObject info_probe) : QStandardItem()
{
    this->name      = info_probe.value("name").toString("undefined");
    this->belong_to = info_probe.value("target").toString("undefined");
    this->r1 = new QStandardItem();
    this->r2 = new QStandardItem("hello");
    this->r3 = new QStandardItem("hello");
    this->r4 = new QStandardItem("hello");
    this->r5 = new QStandardItem("hello");

    this->updateInfo(info_probe);
}


void ProbeItem::updateInfo(QJsonObject info_probe)
{
    this->setText(this->name);
    //this->icon = QPixmap(":/ressources/images/32/logo.png");
    this->icon = QIcon(":/ressources/images/32/logo.png");
}


QVariant ProbeItem::data(int role) const
{
    if (role == Qt::DecorationRole) {return this->icon;}
    if (role == Qt::DisplayRole)  	{return this->name;}

    return QStandardItem::data(role);
}


int ProbeItem::type() const
{
    return 1001;
}
