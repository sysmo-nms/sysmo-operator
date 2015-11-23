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
#include "include/dashboard/dashboardtab.h"

DashboardTab::DashboardTab(QWidget* parent) : NFrameContainer(parent)
{
    NGrid* grid = new NGrid();
    this->setLayout(grid);

    NFrameContainer* buttons_container = new NFrameContainer(this);
    NGridContainer*  buttons_layout = new NGridContainer();
    buttons_container->setLayout(buttons_layout);

    QPushButton* button_save   = new QPushButton(this);
    button_save->setIcon(QIcon(":/icons/document-save.png"));
    QPushButton* button_cancel = new QPushButton(this);
    button_cancel->setIcon(QIcon(":/icons/edit-undo.png"));
    buttons_layout->addWidget(button_save,  0,0);
    buttons_layout->addWidget(button_cancel,0,1);
    buttons_layout->setColumnStretch(0,0);
    buttons_layout->setColumnStretch(1,0);
    buttons_layout->setColumnStretch(2,1);

    grid->addWidget(buttons_container, 0,0);

    QMdiArea* mdi = new QMdiArea(this);
    grid->addWidget(mdi, 1, 0);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);
}

