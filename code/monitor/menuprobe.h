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
#ifndef MENUPROBE_H
#define MENUPROBE_H

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "windows/probewindow.h"
#include "dialogs/messagebox.h"

#include <QMenu>
#include <QWidget>
#include <QString>
#include <QPoint>
#include <QAction>
#include <QVariant>
#include <QMap>

#include <QDebug>


class MenuProbe : public QMenu
{
    Q_OBJECT

public:
    MenuProbe(QWidget* parent = 0);
    void showMenuFor(QString target, QPoint at);

private:
    QString probe_name;

private slots:
    void handleForceProbe();
    void handleForceProbeReply(QVariant reply);
    void handlePauseProbe();
    void handleDeleteProbe();
    void handleDeleteProbeReply(QVariant reply);
    void handleShowPerf();

};

#endif // MENUPROBE_H
