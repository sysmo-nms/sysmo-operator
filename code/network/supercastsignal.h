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
#ifndef SUPERCASTSIGNAL_H
#define SUPERCASTSIGNAL_H

#include <QObject>
#include <QVariant>
#include <QString>

class SupercastSignal : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSignal(QObject* parent = 0);
    void emitServerMessage(QVariant json);
    void emitServerMessage(QString string);
    void emitServerMessage(int integer);

signals:
    void serverMessage(QVariant json);
    void serverMessage(QString  string);
    void serverMessage(int      integer);
};

#endif // SUPERCASTSIGNAL_H
