#include "probeitem.h"

ProbeItem::ProbeItem(QJsonObject info_probe) : QStandardItem()
{
    this->name      = info_probe.value("name").toString("undefined");
    this->belong_to = info_probe.value("target").toString("undefined");
    this->r1 = new QStandardItem();
    this->r2 = new ProgressItem(0,0);
    this->r3 = new QStandardItem();
    this->r4 = new QStandardItem();
    this->r5 = new QStandardItem();

    this->updateInfo(info_probe);
}


void ProbeItem::updateInfo(QJsonObject info_probe)
{
    //this->icon = QPixmap(":/icons/logo.png");
    this->setText(info_probe.value("descr").toString(""));
    QString status = info_probe.value("status").toString("undef");
    if (status == "OK") {
        this->icon = QPixmap(":/pixmaps/weather-clear.png");
    } else if (status == "WARNING") {
        this->icon = QPixmap(":/pixmaps/weather-showers.png");
    } else if (status == "CRITICAL") {
        this->icon = QPixmap(":/pixmaps/weather-severe-alert.png");
    } else if (status == "ERROR") {
        this->icon = QPixmap(":/pixmaps/weather-few-clouds-night.png");
    } else {
        this->icon = QPixmap(":/pixmaps/weather-clear-night.png");
    }
    this->icon = QPixmap(":/pixmaps/weather-clear.png");
    this->r3->setText(info_probe.value("status").toString(""));
    if (info_probe.value("active").toBool()) {
        this->r4->setText("active");
    } else {
        this->r4->setText("paused");
    }
}


QVariant ProbeItem::data(int role) const
{
    if (role == Qt::DecorationRole) {return this->icon;}

    return QStandardItem::data(role);
}


int ProbeItem::type() const
{
    return 1001;
}
