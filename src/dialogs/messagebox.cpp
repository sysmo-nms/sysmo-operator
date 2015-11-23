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
#include "include/dialogs/messagebox.h"

MessageBox::MessageBox(QWidget* parent) : QMessageBox(parent)
{
    /*
    this->setWindowFlags(this->windowFlags() | Qt::WindowStaysOnTopHint);
    QTimer* timer = new QTimer(this);
    timer->setSingleShot(false);
    timer->setInterval(100);
    QObject::connect(
                timer, SIGNAL(timeout()),
                this, SLOT(raise()));
                */
    this->setModal(true);

}



void MessageBox::setIconType(int icon_type)
{
    if (icon_type == Sysmo::MESSAGE_ERROR) {
        this->setIconPixmap(QPixmap(":/box_icons/dialog-error.png"));
        return;
    }

    if (icon_type == Sysmo::MESSAGE_WARNING) {
        this->setIconPixmap(QPixmap(":/box_icons/dialog-warning.png"));
        return;
    }

    if (icon_type == Sysmo::MESSAGE_INFO) {
        this->setIconPixmap(QPixmap(":/box_icons/dialog-information.png"));
        return;
    }
}
