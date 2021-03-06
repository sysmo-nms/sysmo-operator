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
#include "rrd4qtsignal.h"

Rrd4QtSignal::Rrd4QtSignal(QObject* parent) : QObject(parent) {}


void Rrd4QtSignal::emitServerMessage(int integer) {

    emit this->serverMessage(integer);

}


void Rrd4QtSignal::emitServerMessage(QString string) {

    emit this->serverMessage(string);

}


void Rrd4QtSignal::emitServerMessage(QVariant json) {

    emit this->serverMessage(json);

}
