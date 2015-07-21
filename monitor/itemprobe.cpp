#include "itemprobe.h"

int ItemProbe::type() const { return Sysmo::TYPE_PROBE; }

ItemProbe::ItemProbe(QJsonObject info_probe) : QStandardItem()
{
    this->name      = info_probe.value("name").toString("undefined");
    this->belong_to = info_probe.value("target").toString("undefined");
    int step        = info_probe.value("step").toInt(0);

    this->setData(this->name, Sysmo::ROLE_ELEMENT_NAME);
    this->item_progress    = new QStandardItem();
    this->item_progress->setData(1,    Sysmo::ROLE_IS_PROGRESS_ITEM);
    this->item_progress->setData(step, Sysmo::ROLE_PROGRESS_STEP);
    this->item_progress->setData(0,    Sysmo::ROLE_PROGRESS_NEXT);
    this->item_status      = new QStandardItem();
    this->item_state       = new QStandardItem();
    this->item_last_return = new QStandardItem();

    this->updateInfo(info_probe);
}


void ItemProbe::updateInfo(QJsonObject info_probe)
{
    this->setData(info_probe.value("descr").toString(""), Qt::DisplayRole);
    QString status = info_probe.value("status").toString("undef");
    if (status == "OK")
    {
        this->setData(QPixmap(":/pixmaps/weather-clear.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_OK, Sysmo::ROLE_PROBE_STATUS);

    }
    else if (status == "WARNING")
    {
        this->setData(QPixmap(":/pixmaps/weather-showers.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_WARNING, Sysmo::ROLE_PROBE_STATUS);

    }
    else if (status == "CRITICAL")
    {
        this->setData(QPixmap(":/pixmaps/weather-severe-alert.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_CRITICAL, Sysmo::ROLE_PROBE_STATUS);

    }
    else if (status == "ERROR")
    {
        this->setData(QPixmap(":/pixmaps/weather-few-clouds-night.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_ERROR, Sysmo::ROLE_PROBE_STATUS);

    }
    else
    {
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"),
                                                Qt::DecorationRole);
        this->setData(Sysmo::STATUS_UNKNOWN, Sysmo::ROLE_PROBE_STATUS);
    }

    this->item_status->setData(status, Qt::DisplayRole);

    if (info_probe.value("active").toBool())
    {
        this->item_state->setData("Active", Qt::DisplayRole);
        /*this->item_state->setData(QPixmap(":/pixmaps/media-playback-start"),
                                  Qt::DecorationRole);
                                  */
    }
    else
    {
        this->item_state->setData("Paused", Qt::DisplayRole);
        /*
        this->item_state->setData(QPixmap(":/pixmaps/media-playback-pause"),
                                  Qt::DecorationRole);
                                  */
    }

    this->setData("hello", Sysmo::ROLE_FILTER_STRING);
}


void ItemProbe::updateReturnInfo(QJsonObject info)
{
    QString reply = info.value("replyString").toString("undefined");
    this->item_last_return->setData(reply, Qt::DisplayRole);
    int in_sec      = info.value("nextReturn").toInt(0) / 1000;
    int current_sec = QDateTime::currentMSecsSinceEpoch() / 1000;
    int next_in_sec = current_sec + in_sec;
    this->item_progress->setData(next_in_sec, Sysmo::ROLE_PROGRESS_NEXT);
    this->emitDataChanged();
}


