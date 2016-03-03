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
#include "statusbutton.h"

StatusButton::StatusButton(QWidget *parent, QString type, QPixmap pixmap)
        : QPushButton(parent)
{
    this->red = false;
    this->type = type;
    this->counter = 0;
    this->setFixedHeight(35);
    this->setToolTip(type);
    this->lcd = new QLCDNumber(this);
    this->lcd->setSegmentStyle(QLCDNumber::Flat);
    this->lcd->setFrameShape(QFrame::StyledPanel);
    //this->lcd->setFrameShadow(QFrame::Plain);
    NGrid* grid = new NGrid();

    QLabel* lab = new QLabel(this);
    lab->setPixmap(pixmap);

    grid->addWidget(lab, 0,0);
    grid->addWidget(this->lcd, 0,1);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    this->setLayout(grid);
    QObject::connect(
                this, SIGNAL(clicked(bool)),
                this, SLOT(updateText()));
    this->lcd->setStyleSheet("");
}

void StatusButton::increment()
{
    this->counter += 1;
    this->lcd->display(this->counter);
}

void StatusButton::decrement()
{
    this->counter -= 1;
    this->lcd->display(this->counter);
    if (this->counter == 0) {
        this->lcd->setStyleSheet("");
    }
}

void StatusButton::updateText()
{
    QString filter = "status:%1";
    emit this->setText(filter.arg(this->type));
}

void StatusButton::toggleRed()
{
    if (this->counter > 0) {
        if (this->red) {
            this->lcd->setStyleSheet("");
            this->red = false;
        } else {
            this->lcd->setStyleSheet("QFrame {border: 2px solid #ef2929;}");
            this->red = true;
        }
    }
}
