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
#include "logswidget.h"

#include <widgets/ngridcontainer.h>

#include <QObject>
#include <QLabel>

// TODO

LogsWidget::LogsWidget(QWidget *parent) : NFrame(parent) {

    NGridContainer* grid = new NGridContainer();
    this->setLayout(grid);
    grid->addWidget(new QLabel("hello", this), 0, 0);

}

LogsWidget::~LogsWidget() {

}
