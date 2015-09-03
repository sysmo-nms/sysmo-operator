#include "itemtarget.h"

int ItemTarget::type() const { return Sysmo::TYPE_TARGET; }

ItemTarget::ItemTarget(QJsonObject info_target) : QStandardItem()
{
    this->updateInfo(info_target);
    this->updateIconStatus();
}

void ItemTarget::updateProbeFilter(QString probe_name, QJsonObject obj)
{
    this->filter_hash.insert(probe_name,
          QJsonDocument(obj).toJson(QJsonDocument::Compact));
    this->updateFilter();
}

void ItemTarget::deleteProbeFilter(QString probe_name)
{
    this->filter_hash.remove(probe_name);
    this->updateFilter();
}

void ItemTarget::updateFilter() {
    QString str = this->orig_filter;
    QHashIterator<QString, QString> i(this->filter_hash);
    while(i.hasNext()) {
        i.next();
        str = str + i.value();
    }
    this->setData(str, Sysmo::ROLE_FILTER_STRING);
}

void ItemTarget::updateInfo(QJsonObject info_target)
{
    this->name              = info_target.value("name").toString("undefined");
    this->target_properties = info_target.value("properties").toObject();

    this->setData(this->name, Sysmo::ROLE_ELEMENT_NAME);

    QString hostname   = this->target_properties.value("host").toString("undefined");
    QString fixed_name = this->target_properties.value("name").toString("undefined");
    QString sys_name   = this->target_properties.value("sysName").toString("undefined");

    QString display;

    if (sys_name != "undefined")
    {
        display.append(sys_name);
        display.append(QString("  (%1)").arg(hostname));
    }
    else if ((fixed_name != "undefined") & (fixed_name != ""))
    {
        display.append(fixed_name);
        display.append(QString("  (%1)").arg(hostname));
    }
    else
    {
        display.append(hostname);
    }

    this->setData(display, Qt::DisplayRole);

    this->orig_filter = QJsonDocument(info_target).toJson(QJsonDocument::Compact);
    this->setData(this->orig_filter, Sysmo::ROLE_FILTER_ORIG);
    this->updateFilter();
    this->updateTooltip();
}

void ItemTarget::updateTooltip()
{
    QString tooltip;
    QStringList keys = this->target_properties.keys();
    keys.sort();
    QStringListIterator it(keys);
    tooltip += "<table>";
    while (it.hasNext()) {
        QString key = it.next();
        QString val = this->target_properties.value(key).toString();
        tooltip += "<tr><td><b>" + key + "</b></td><td>: " + val + "</td></tr>";
    }
    tooltip += "</table>";
    this->setToolTip(tooltip);
}

void ItemTarget::updateIconStatus()
{
    int status = 0;
    for (int i = 0; i < this->rowCount(); i ++)
    {
        int pstatus = this->child(i, 0)->data(Sysmo::ROLE_PROBE_STATUS)
                                                     .toInt(NULL);
        if (pstatus > status) {status = pstatus;}
    }
    if (status == Sysmo::STATUS_OK)
    {
        this->setData(QPixmap(":/pixmaps/weather-clear.png"), Qt::DecorationRole);
    }
    else if (status == Sysmo::STATUS_UNKNOWN)
    {
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"), Qt::DecorationRole);
    }
    else if (status == Sysmo::STATUS_ERROR)
    {
        this->setData(QPixmap(":/pixmaps/weather-few-clouds-night.png"), Qt::DecorationRole);
    }
    else if (status == Sysmo::STATUS_WARNING)
    {
        this->setData(QPixmap(":/pixmaps/weather-showers.png"), Qt::DecorationRole);
    }
    else if (status == Sysmo::STATUS_CRITICAL)
    {
        this->setData(QPixmap(":/pixmaps/weather-severe-alert.png"), Qt::DecorationRole);
    }
}


