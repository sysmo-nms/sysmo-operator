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
#include "statusbutton.h"
#include "ngridcontainer.h"
#include "ngrid.h"

#include <QObject>
#include <QLCDNumber>
#include <QLabel>
#include <QFrame>
#include <QPalette>
#include <QDebug>

/**
 * Status button including a layout to show an image status,
 * a counter, and blinking border if the status is not OK
 */
StatusButton::StatusButton(QWidget *parent, QString type, QIcon icon)
: QPushButton(parent) {

    this->red = false;
    this->type = type;
    this->counter = 0;
    this->setToolTip("Quick filter: only " + type);
    this->setIcon(icon);
    this->setIconSize(QSize(25, 25));
    this->setFlat(true);
    this->setStyleSheet("QPushButton {border: 2px solid rgba(0,0,0,0);}");

    QObject::connect(
            this, SIGNAL(clicked(bool)),
            this, SLOT(updateText()));

}

void StatusButton::increment() {

    this->counter += 1;

}

void StatusButton::decrement() {

    this->counter -= 1;

}

void StatusButton::updateText() {

    QString filter = "status:%1";
    emit this->setText(filter.arg(this->type));

}

void StatusButton::toggleRed() {

    if (this->counter > 0) {
        if (this->red) {
            this->setStyleSheet("QPushButton {border: 2px solid rgba(0,0,0,0);}");
            this->red = false;
        } else {
            this->setStyleSheet("QPushButton {border: 2px solid #ef2929;}");
            this->red = true;
        }
    }

}
