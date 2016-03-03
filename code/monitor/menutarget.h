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
#ifndef MENUTARGET_H
#define MENUTARGET_H

#include "../sysmo.h"
#include "monitor.h"
#include "../dialogs/messagebox.h"
#include "../network/supercast.h"
#include "../network/supercastsignal.h"
#include "../actions/monitoractions.h"

#include <QObject>
#include <QWidget>
#include <QString>
#include <QMenu>
#include <QPoint>
#include <QAction>
#include <QIcon>
#include <QMessageBox>
#include <QVariant>
#include <QMap>

#include <QDebug>

class MenuTarget : public QMenu
{
    Q_OBJECT

public:
    MenuTarget(QWidget* parent = 0);
    void showMenuFor(QString target, QPoint at);

private:
    QString target_name;
    //QMenu*  operation_menu;

private slots:
    void connectNewProbeDialog();
    void deleteTarget();
    void deleteTargetReply(QVariant reply);
    void handleOperatorActionsConfig();

signals:
    void openNewProbeDialog(QString target);
};

#endif // MENUTARGET_H
