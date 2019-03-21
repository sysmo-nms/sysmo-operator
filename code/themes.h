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
#ifndef THEMES_H
#define THEMES_H

#include <QPalette>
#include <QString>

class Themes {
public:
    static QPalette midnight;
    static QPalette inland;
    static QPalette greys;
    static QPalette iced;
    static QString style_used;
    static void setStyle(QString style);
    static QString getStyleSheet();

private:
    static QPalette initMidnight();
    static QPalette initInland();
    static QPalette initGreys();
    static QPalette initIced();
};

#endif // THEMES_H
