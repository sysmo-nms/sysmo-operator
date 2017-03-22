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
#include "monitoractionconfig.h"
#include <widgets/ngrid.h>
#include <widgets/nframe.h>
#include <widgets/ngridcontainer.h>

#include <QTreeWidgetItem>
#include <QStringList>
#include <QLabel>
#include <QDialogButtonBox>
#include <QPushButton>

MonitorActionConfig::MonitorActionConfig(QWidget* parent, QString target)
: QDialog(parent) {

    this->target = target;
    this->setMinimumHeight(200);
    this->setMinimumWidth(500);


    QLabel *label = new QLabel(this);
    label->setText("Configure actions tool");
    this->tree_widget = new QTreeWidget(this);
    QStringList header;
    header << "Name" << "Executable" << "Default";
    this->tree_widget->setHeaderLabels(header);

    QDialogButtonBox *buttonBox = new QDialogButtonBox(this);
    buttonBox->addButton(QDialogButtonBox::Close);
    QPushButton *close = buttonBox->button(QDialogButtonBox::Close);
    QObject::connect(
            close, SIGNAL(clicked(bool)),
            this, SLOT(close()));

    NFrame *frame = new NFrame(this);

    NGrid *grid = new NGrid();
    frame->setLayout(grid);
    grid->addWidget(label, 0, 0);
    grid->addWidget(this->tree_widget, 1, 0);
    grid->addWidget(buttonBox, 2, 0);


    NGridContainer *grid_container = new NGridContainer(this);
    grid_container->addWidget(frame);


}

