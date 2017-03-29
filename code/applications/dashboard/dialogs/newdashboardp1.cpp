/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
#include "newdashboardp1.h"

#include <QWizard>
#include <QCommandLinkButton>
#include <QButtonGroup>
#include <QPixmap>
#include <QLabel>

#include <widgets/ngrid.h>
#include <widgets/nframe.h>

NewDashboardP1::NewDashboardP1(QWidget* parent) : QWizardPage(parent) {

    this->setTitle("Create a new Dashboard");
    this->setSubTitle("Please select the type of dashboard you want to create");
    this->setFinalPage(true);

    NFrame *left = new NFrame(this);
    left->setFixedWidth(300);

    QPixmap right_pix(":/images/perf_view.png");
    QLabel *right = new QLabel(this);
    right->setFixedHeight(300);
    right->setFixedWidth(300);
    right->setPixmap(right_pix);
    right->setScaledContents(true);

    NGrid *grid = new NGrid(this);
    this->setLayout(grid);

    grid->addWidget(left, 0, 0);
    grid->addWidget(right, 0, 1);
    grid->setColumnStretch(0, 1);
    grid->setColumnStretch(1, 1);

    NGrid *lgrid = new NGrid(left);
    left->setLayout(lgrid);

    QCommandLinkButton *perf_view = new QCommandLinkButton(left);
    perf_view->setCheckable(true);
    perf_view->setText("Performance View");
    perf_view->setDescription("Create a stack of linkend performances graphics from any target/probes you want.");

    QCommandLinkButton *status_view = new QCommandLinkButton(left);
    status_view->setCheckable(true);
    status_view->setText("Status View");
    status_view->setDescription("Create a map of probes/target status with labels and shapes.");

    QCommandLinkButton *map_view = new QCommandLinkButton(left);
    map_view->setCheckable(true);
    map_view->setText("Map View");
    map_view->setDescription("Show your managed elements on a OSM or Google map.");

    QCommandLinkButton *composition_view = new QCommandLinkButton(left);
    composition_view->setCheckable(true);
    composition_view->setText("Composition");
    composition_view->setDescription("Compose a dashboard with any of the above views into one.");


    QCommandLinkButton *roundrobin_view = new QCommandLinkButton(left);
    roundrobin_view->setCheckable(true);
    roundrobin_view->setText("Round Robin");
    roundrobin_view->setDescription("Compose a display with any of the above views into one rotating at a defined interval.");

    QButtonGroup *group = new QButtonGroup(left);
    group->addButton(perf_view);
    group->addButton(status_view);
    group->addButton(map_view);
    group->addButton(composition_view);
    group->addButton(roundrobin_view);
    group->setExclusive(true);
    perf_view->setChecked(true);

    lgrid->addWidget(perf_view, 0,0);
    lgrid->addWidget(status_view, 1,0);
    lgrid->addWidget(map_view, 2,0);
    lgrid->addWidget(composition_view, 3,0);
    lgrid->addWidget(roundrobin_view, 4,0);
    lgrid->setRowStretch(0,0);
    lgrid->setRowStretch(1,0);
    lgrid->setRowStretch(2,0);
    lgrid->setRowStretch(3,0);
    lgrid->setRowStretch(4,0);
    lgrid->setRowStretch(5,1);

}
