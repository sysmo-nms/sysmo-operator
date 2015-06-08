#include "probeitem.h"

int ProbeItem::type() const { return Sysmo::TYPE_PROBE; }

ProbeItem::ProbeItem(QJsonObject info_probe) : QStandardItem()
{
    this->name      = info_probe.value("name").toString("undefined");
    this->belong_to = info_probe.value("target").toString("undefined");
    int step = info_probe.value("step").toInt(0);
    this->r1 = new QStandardItem();
    this->r2 = new QStandardItem();
    this->r2->setData(1,    Sysmo::ROLE_IS_PROGRESS_ITEM);
    this->r2->setData(step, Sysmo::ROLE_PROGRESS_STEP);
    this->r2->setData(0,    Sysmo::ROLE_PROGRESS_NEXT);
    this->r3 = new QStandardItem();
    this->r4 = new QStandardItem();
    this->r5 = new QStandardItem();

    this->updateInfo(info_probe);
}


void ProbeItem::updateInfo(QJsonObject info_probe)
{
    this->setData(info_probe.value("descr").toString(""), Qt::DisplayRole);
    QString status = info_probe.value("status").toString("undef");
    if (status == "OK") {
        this->setData(QPixmap(":/pixmaps/weather-clear.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_OK, Sysmo::ROLE_PROBE_STATUS);

    } else if (status == "WARNING") {
        this->setData(QPixmap(":/pixmaps/weather-showers.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_WARNING, Sysmo::ROLE_PROBE_STATUS);

    } else if (status == "CRITICAL") {
        this->setData(QPixmap(":/pixmaps/weather-severe-alert.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_CRITICAL, Sysmo::ROLE_PROBE_STATUS);

    } else if (status == "ERROR") {
        this->setData(QPixmap(":/pixmaps/weather-few-clouds-night.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_ERROR, Sysmo::ROLE_PROBE_STATUS);

    } else {
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_UNKNOWN, Sysmo::ROLE_PROBE_STATUS);
    }

    this->r3->setData(status, Qt::DisplayRole);

    if (info_probe.value("active").toBool())
        this->r4->setData("active", Qt::DisplayRole);
    else
        this->r4->setData("paused", Qt::DisplayRole);
}


void ProbeItem::updateReturnInfo(QJsonObject info)
{
    QString reply = info.value("replyString").toString("undefined");
    this->r5->setData(reply, Qt::DisplayRole);
    int in_sec      = info.value("nextReturn").toInt(0) / 1000;
    int current_sec = QDateTime::currentMSecsSinceEpoch() / 1000;
    int next_in_sec = current_sec + in_sec;
    this->r2->setData(next_in_sec, Sysmo::ROLE_PROGRESS_NEXT);
    this->emitDataChanged();
}


