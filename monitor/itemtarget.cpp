#include "itemtarget.h"

int ItemTarget::type() const { return Sysmo::TYPE_TARGET; }

ItemTarget::ItemTarget(QMap<QString,QVariant> info_target) : QStandardItem()
{
    this->updateInfo(info_target);
    this->updateIconStatus();
}

void ItemTarget::updateProbeFilter(QString probe_name, QMap<QString,QVariant> obj)
{
    this->filter_hash.insert(probe_name, QJson::encode(obj));
    this->updateFilter();
}

void ItemTarget::deleteProbeFilter(QString probe_name)
{
    this->filter_hash.remove(probe_name);
    this->updateFilter();
}

void ItemTarget::updateFilter() {
    QString str = this->orig_filter;
    QMapIterator<QString, QString> i(this->filter_hash);
    while(i.hasNext()) {
        i.next();
        str = str + i.value();
    }
    this->setData(str.remove("\""), Sysmo::ROLE_FILTER_STRING);
}

void ItemTarget::updateInfo(QMap<QString,QVariant> info_target)
{
    this->name              = info_target.value("name").toString();
    this->target_properties = info_target.value("properties").toMap();

    this->setData(this->name, Sysmo::ROLE_ELEMENT_NAME);

    QString hostname   = this->target_properties.value("host").toString();
    QString fixed_name = this->target_properties.value("name").toString();
    QString sys_name   = this->target_properties.value("sysName").toString();

    QString display;

    if ((!sys_name.isEmpty()) & (sys_name != "undefined")) {
        display.append(sys_name);
        display.append(QString("  (%1)").arg(hostname));
    } else if ((!fixed_name.isEmpty()) & (fixed_name != "")) {
        display.append(fixed_name);
        display.append(QString("  (%1)").arg(hostname));
    } else {
        display.append(hostname);
    }

    this->setData(display, Qt::DisplayRole);

    this->orig_filter = QJson::encode(info_target);
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
    if (this->rowCount() == 0) {
        this->setData(QPixmap(":/pixmaps/weather-clear-night.png"), Qt::DecorationRole);
        return;
    }

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


