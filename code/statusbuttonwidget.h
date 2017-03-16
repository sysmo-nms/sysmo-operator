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
#ifndef STATUSBUTTONWIDGET_H
#define STATUSBUTTONWIDGET_H

#include "nframecontainer.h"
#include "statusbutton.h"

#include <QWidget>
#include <QString>
#include <QVariant>

class StatusButtonWidget : public NFrameContainer {
    Q_OBJECT
public:
    StatusButtonWidget(QWidget* parent);
    StatusButton* warn;
    StatusButton* crit;
    StatusButton* err;


private:
    QMap<QString, QString>* status_map;
    void incrementStatus(QString status);
    void decrementStatus(QString status);

public slots:
    void handleDeleteProbe(QVariant obj);
    void handleInfoProbe(QVariant obj);

};

#endif // STATUSBUTTONWIDGET_H
