#ifndef MONITORACTIONS_H
#define MONITORACTIONS_H

#include "actions/monitoractionsdialog.h"
#include "actions/monitoractionconfig.h"

#include "monitor/monitor.h"

#include <QDebug>
#include <QSettings>
#include <QVariant>
#include <QJsonObject>

class MonitorActions
{
public:
    static void openActionFor(QString target);

};

#endif // MONITORACTIONS_H
