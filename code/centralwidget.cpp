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
#include "centralwidget.h"

CentralWidget::CentralWidget(QWidget* parent) : NFrameContainer(parent)
{
    // Left selector
    NFrameContainer* selector = new NFrameContainer(this);
    selector->setFixedWidth(30);
    selector->setContentsMargins(0,2,0,2);

    SideButton* monitor_button   = new SideButton(this);
    monitor_button->setIconSize(QSize(32,115));
    monitor_button->setIcon(QIcon(":/images/monitor-black.png"));
    /* TODO
    SideButton* dashboard_button = new SideButton(this);
    dashboard_button->setIconSize(QSize(32,115));
    dashboard_button->setIcon(QIcon(":/images/dashboard-black.png"));
    */

    QButtonGroup* selector_group = new QButtonGroup(this);
    selector_group->addButton(monitor_button,   CentralWidget::APP_MONITOR);
    //selector_group->addButton(dashboard_button, CentralWidget::APP_DASHBOARD);
    selector_group->setExclusive(true);
    monitor_button->setCheckable(true);
    //dashboard_button->setCheckable(true);

    NGridContainer* selector_grid = new NGridContainer();
    selector->setLayout(selector_grid);
    selector_grid->setVerticalSpacing(4);
    selector_grid->addWidget(monitor_button,  0,0);
    //selector_grid->addWidget(dashboard_button,1,0);

    // Right stack
    NFrameContainer* stack        = new NFrameContainer(this);
    QStackedLayout*  stack_layout = new QStackedLayout();
    MonitorWidget*   monitor   = new MonitorWidget(this);
    DashboardWidget* dashboard = new DashboardWidget(this);
    stack_layout->setContentsMargins(0,0,0,0);
    stack_layout->insertWidget(CentralWidget::APP_MONITOR,   monitor);
    stack_layout->insertWidget(CentralWidget::APP_DASHBOARD, dashboard);
    stack->setLayout(stack_layout);

    // Connect stack and selector
    stack_layout->setCurrentIndex(CentralWidget::APP_MONITOR);
    monitor_button->setChecked(true);
    QObject::connect(
                selector_group, SIGNAL(buttonClicked(int)),
                stack_layout,   SLOT(setCurrentIndex(int)));

    // Final grid
    NGrid* grid = new NGrid();
    this->setLayout(grid);
    grid->setHorizontalSpacing(5);
    grid->setVerticalSpacing(5);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    grid->addWidget(selector, 0,0);
    grid->addWidget(stack,    0,1);
}
