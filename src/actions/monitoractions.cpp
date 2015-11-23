/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "include/actions/monitoractions.h"

void MonitorActions::openActionFor(QString target)
{
    qDebug() << "open action for" << target;

    QSettings s;
    QVariant var = s.value("actions/monitoractions");

    // if settings is initialized
    if (var.isValid())
    {
        QMap<QString, QVariant> dict = var.toMap();
        QVariant tval = dict.value(target);

        // if tval is valid hence have at least one action execute it
        if (tval.isValid()) {
            //return;
            qDebug() << "should execute action and exit?";
        }
    } else {
        /*
         * Initialize empty QMap<QString,QVariant>
         */
        s.setValue("actions/monitoractions", QMap<QString,QVariant>());
        s.sync();
    }

    /*
     * No suitable action to launch.
     *
     * For the dial to be shown on the center of the application rect, use
     * MonitorWidget instance has parent
     */
    MonitorActionsDialog* dial =
       new MonitorActionsDialog(
                Monitor::getCenterWidget(), target);
    dial->open();
}
