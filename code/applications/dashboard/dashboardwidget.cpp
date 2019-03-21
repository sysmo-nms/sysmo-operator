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
#include "dashboardwidget.h"
#include "dashboardtab.h"

#include <widgets/ngridcontainer.h>
#include <QObject>
#include <QTabWidget>
#include <QTabBar>
#include <QLabel>
#include <QPushButton>
#include <QIcon>

// TODO

DashboardWidget::DashboardWidget(QWidget *parent) : NFrame(parent) {

    NGridContainer* grid = new NGridContainer();
    this->setLayout(grid);

    QTabWidget* tab = new QTabWidget(this);
    // tabBar() in qt4 is protected
    /*
    QTabBar* tab_bar = tab->tabBar();
    tab_bar->setUsesScrollButtons(true);
    tab_bar->setExpanding(true);
     */

    QPushButton* button_add = new QPushButton(this);
    button_add->setIcon(QIcon(":/icons/list-add.png"));
    button_add->setFlat(true);
    tab->setCornerWidget(button_add, Qt::TopLeftCorner);

    QPushButton* button_help = new QPushButton(this);
    button_help->setIcon(QIcon(":/icons/dialog-information.png"));
    button_help->setFlat(true);
    tab->setCornerWidget(button_help, Qt::TopRightCorner);

    grid->addWidget(tab, 0, 0);
    DashboardTab* dash_tab = new DashboardTab(this);
    tab->addTab(dash_tab, "Tab 1");

}

DashboardWidget::~DashboardWidget() {

}
