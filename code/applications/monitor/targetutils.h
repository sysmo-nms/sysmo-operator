/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

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
#ifndef TARGETUTILS_H
#define TARGETUTILS_H
#include <QMap>
#include <QVariant>
#include <QString>
#include <QVariant>

class TargetUtils {
public:
    static QString getName(QMap<QString, QVariant> properties) {
        QString hostname = properties.value("host").toString();
        QString fixed_name = properties.value("name").toString();
        QString sys_name = properties.value("sysName").toString();

        QString display;

        if ((!sys_name.isEmpty()) & (sys_name != "undefined")) {
            display.append(sys_name);
            display.append(QString("  (%1)").arg(hostname));
        } else if ((!fixed_name.isEmpty()) & (fixed_name != "")) {
            display.append(fixed_name);
            display.append(QString("  (%1)").arg(hostname));
        } else {
            display.append(hostname);
        }
        return display;
    }
};

#endif // TARGETUTILS_H
