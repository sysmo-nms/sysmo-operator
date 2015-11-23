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
#include "include/dialogs/newtarget.h"

NewTarget::NewTarget(QWidget* parent) : QWizard(parent)
{
    this->setWindowTitle("New target");
    this->setModal(true);
    this->setOption(QWizard::NoBackButtonOnLastPage, true);
    this->setButtonText(QWizard::FinishButton, "Validate");
    this->setButtonText(QWizard::CancelButton, "Close");
    this->setWizardStyle(QWizard::ModernStyle);

    NewTargetPage1* page1 = new NewTargetPage1(this);
    this->setPage(1, page1);
    this->setStartId(1);
    this->setFixedWidth(525);
}
