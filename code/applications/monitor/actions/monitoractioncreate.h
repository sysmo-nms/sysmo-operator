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
#ifndef MONITORACTIONCREATE_H
#define MONITORACTIONCREATE_H

#include <widgets/lineedit.h>

#include <QDialog>
#include <QWidget>
#include <QHash>
#include <QString>
#include <QVariant>
#include <QPushButton>

class MonitorActionCreate : public QDialog {
    Q_OBJECT
public:
    explicit MonitorActionCreate(QWidget *parent = 0);
    explicit MonitorActionCreate(
            QString name, QHash<QString, QVariant> conf, QWidget *parent = 0);

    LineEdit *name;
    LineEdit *cmd;
    LineEdit *args;

private:
    QPushButton *apply;
    void initLayout();
signals:

public slots:
    void handleSearchExe();
    void handleEditOk();
};

#endif // MONITORACTIONCREATE_H
