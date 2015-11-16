#ifndef MONITORACTIONS_H
#define MONITORACTIONS_H

#include "include/actions/monitoractionsdialog.h"
#include "include/actions/monitoractionconfig.h"

#include "include/monitor/monitor.h"

#include <QDebug>
#include <QSettings>
#include <QVariant>

class MonitorActions
{
public:
    static void openActionFor(QString target);

};

#endif // MONITORACTIONS_H
