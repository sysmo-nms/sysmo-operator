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
#include "newdashboard.h"
#include "newdashboardp1.h"

#include <QObject>

NewDashboard::NewDashboard(QWidget* parent) : QWizard(parent) {

    this->setWindowTitle("New Dashboard");
    this->setModal(true);
    this->setOption(QWizard::NoBackButtonOnLastPage, true);
    this->setButtonText(QWizard::FinishButton, "Create");
    this->setButtonText(QWizard::CancelButton, "Cancel");

    this->setMinimumHeight(300);
    this->setMinimumWidth(300);

    NewDashboardP1 *p1 = new NewDashboardP1(this);
    this->setPage(1, p1);
    this->setStartId(1);

}
