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
#ifndef ROTATINGFILELOGGER_H
#define ROTATINGFILELOGGER_H

#include "stdio.h"
#include "stdlib.h"

#include <QMutex>
#include <QObject>
#include <QString>
#include <QDesktopServices>
#include <QDebug>
#include <QDir>
#include <QCoreApplication>
#include <QThread>
#include <QByteArray>
#include <QIODevice>

#if QT_VERSION >= 0x050000
#include <QMessageLogContext>
#endif

class RotatingFileLogger : public QObject
{
public:
    explicit RotatingFileLogger(QObject* parent = 0);
    ~RotatingFileLogger();
    static RotatingFileLogger* getLogger();

#if QT_VERSION >= 0x050000
    static void log(
            QtMsgType type,
            const QMessageLogContext &context,
            const QString &msg);
#else
    static void log(
            QtMsgType type,
            const char *msg);
#endif

private:
    static RotatingFileLogger* singleton;
    static QMutex mtx;
    QString lock;
    QFile*  logFile;
};

#endif // ROTATINGFILELOGGER_H
