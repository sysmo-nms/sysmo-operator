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
#ifndef ACTIONPROCESS_H
#define ACTIONPROCESS_H

#include "include/systemtray.h"

#include <QObject>
#include <QProcess>
#include <QDebug>
#include <QSystemTrayIcon>

class ActionProcess : public QProcess
{
    Q_OBJECT
public:
    ActionProcess(QObject *parent = 0);
    void startProcess(const QString program, const QStringList arguments);

private:
    QString error_string;
    QString programString;
    QStringList programArgs;

private slots:
    void handleErrorMsg();
    void handleStartError(QProcess::ProcessError);
};

#endif // ACTIONPROCESS_H
