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
#include "newprobe.h"

#include "newprobepage1.h"
#include "newprobepage2.h"
#include "newprobepage3.h"

#include <QDebug>

NewProbe::NewProbe(QString forTarget, QWidget* parent) : QWizard(parent) {

    this->setWindowTitle("New probe");
    this->setModal(true);
    this->setButtonText(QWizard::FinishButton, "Validate");
    this->setButtonText(QWizard::CancelButton, "Close");
    this->setWizardStyle(QWizard::ModernStyle);
    this->setMinimumWidth(800);
    this->setMinimumHeight(600);

    NewProbePage1* page1 = new NewProbePage1(forTarget, this);
    NewProbePage2* page2 = new NewProbePage2(forTarget, this);
    // TODO Simulate check
    //NewProbePage3* page3 = new NewProbePage3(this);
    this->setPage(1, page1);
    this->setPage(2, page2);
    //this->setPage(3, page3);
    this->setStartId(1);

}
