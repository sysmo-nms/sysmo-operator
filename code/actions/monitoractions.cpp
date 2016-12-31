/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

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
#include "monitoractions.h"


void MonitorActions::openActionFor(QString target)
{

    qDebug() << "open action for" << target;

    QSettings actions_settings;
    QVariant variant_actions_settings = actions_settings.value("actions/monitoractions");

    // if settings is initialized
    if (variant_actions_settings.isValid())
    {
        QMap<QString, QVariant> dict_actions_settings =
                                               variant_actions_settings.toMap();
        QVariant target_actions = dict_actions_settings.value(target);

        // if tval is valid hence have at least one action execute it
        if (target_actions.isValid()) {
            //return;
            qDebug() << "should execute action and exit?";
        }

    } else {
        /*
         * Initialize empty QMap<QString,QVariant>
         */
        actions_settings.setValue("actions/monitoractions", QMap<QString,QVariant>());
        actions_settings.sync();
    }

    /*
     * No suitable action to launch.
     *
     * For the dial to be shown on the center of the application rect, use
     * MonitorWidget instance has parent
     */
    MonitorActionsDialog* dialog =
       new MonitorActionsDialog(
                Monitor::getCenterWidget(), target);
    dialog->open();
}
