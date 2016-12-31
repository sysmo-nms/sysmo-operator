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
#include "actionprocess.h"


ActionProcess::ActionProcess(QObject *parent)
    : QProcess(parent)
{

    QObject::connect(
                this, SIGNAL(finished(int)),
                this, SLOT(deleteLater()));

    QObject::connect(
                this, SIGNAL(error(QProcess::ProcessError)),
                this, SLOT(handleStartError(QProcess::ProcessError)));

    QObject::connect(
                this, SIGNAL(readyReadStandardError()),
                this, SLOT(handleErrorMsg()));

}

void
ActionProcess::startProcess(const QString program, const QStringList arguments)
{
    this->programString = program;
    this->programArgs = arguments;
    this->start(program,arguments);
}

void
ActionProcess::handleStartError(QProcess::ProcessError err)
{
    QString str;
    str += this->programString;
    str += " ";
    str += this->programArgs.join(" ");
    str += "\n\n";

    switch(err) {
    case QProcess::FailedToStart:
        str += "The process failed to start. Either the invoked program is missing, or you may have insufficient permissions to invoke the program.";
        break;
    case QProcess::Crashed:
        str += "The process crashed some time after starting successfully.";
        break;
    case QProcess::Timedout:
        str += "The last waitFor...() function timed out. The state of QProcess is unchanged, and you can try calling waitFor...() again.";
        break;
    case QProcess::WriteError:
        str += "An error occurred when attempting to write to the process. For example, the process may not be running, or it may have closed its input channel.";
        break;
    case QProcess::ReadError:
        str += "An error occurred when attempting to read from the process. For example, the process may not be running.";
        break;
    default:
        str += "An unknown error occurred. This is the default return value of error().";
        break;
    }

    SystemTray::singleton->showMessage("Start action error", str,
                                       QSystemTrayIcon::Critical, 10000);
}

void
ActionProcess::handleErrorMsg()
{
    this->error_string += QString(this->readAllStandardError());

    QString str;
    str += this->programString;
    str += " ";
    str += this->programArgs.join(" ");
    str += "\n\n";
    str += this->error_string;

    SystemTray::singleton->showMessage(
                "Start action stderr msg", str,
                                       QSystemTrayIcon::Warning, 5000);
}
