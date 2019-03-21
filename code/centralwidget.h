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
#ifndef CENTRALWIDGET_H
#define CENTRALWIDGET_H

#include <widgets/nframecontainer.h>

class CentralWidget : public NFrameContainer {
private:
    static const int APP_MONITOR = 0;
    static const int APP_LOGS = 1;
    static const int APP_DASHBOARD = 2;

public:
    explicit CentralWidget(QWidget* parent = 0);
};

#endif // CENTRALWIDGET_H
