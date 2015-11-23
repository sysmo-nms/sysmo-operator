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
#ifndef MONITORACTIONSDIALOG_H
#define MONITORACTIONSDIALOG_H

#include "include/ngrid.h"
#include "include/nframe.h"
#include "include/actions/monitoractioncreate.h"
#include "include/dialogs/messagebox.h"
#include "include/actions/actionprocess.h"

#include <QDialog>
#include <QWidget>
#include <QObject>
#include <QLabel>
#include <QSettings>
#include <QVariant>
#include <QHash>
#include <QDebug>
#include <QPushButton>
#include <QListWidget>
#include <QIcon>
#include <QDialogButtonBox>
#include <QHashIterator>
#include <QListWidgetItem>
#include <QStringList>

class MonitorActionsDialog : public QDialog
{
    Q_OBJECT
public:
    explicit MonitorActionsDialog(QWidget* parent, QString target);

private:
    QString target;
    QListWidget *list_view;
    void updateView();
    QPushButton *editAction;
    QPushButton *delAction;

public slots:
    void handleAddAction();
    void handleDelAction();
    void handleEditAction();

    void handleDoubleClicked(QListWidgetItem *item);
    void handleSelectionChange();
};

#endif // MONITORACTIONSDIALOG_H
