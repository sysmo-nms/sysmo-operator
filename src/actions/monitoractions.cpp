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
