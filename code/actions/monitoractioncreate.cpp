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
#include "monitoractioncreate.h"

MonitorActionCreate::MonitorActionCreate(
        QString name, QHash<QString, QVariant> conf, QWidget *parent)
                : QDialog(parent)
{
    this->initLayout();
    this->name->setText(name);
    this->cmd->setText(conf.value("cmd").toString());
    this->args->setText(conf.value("args").toString());
}

MonitorActionCreate::MonitorActionCreate(QWidget *parent)
    : QDialog(parent)
{
    this->initLayout();
}

void MonitorActionCreate::initLayout()
{
    NFrameContainer *fr = new NFrameContainer(this);

    NGrid *grid = new NGrid();
    this->setLayout(grid);
    this->setMinimumWidth(500);

    this->name = new LineEdit(this);
    this->cmd = new LineEdit(this);
    this->args = new LineEdit(this);

    QObject::connect(
                this->name, SIGNAL(textChanged(QString)),
                this, SLOT(handleEditOk()));
    QObject::connect(
                this->cmd, SIGNAL(textChanged(QString)),
                this, SLOT(handleEditOk()));


    QFormLayout* form = new QFormLayout();
    fr->setLayout(form);


    form->addRow("Name:", this->name);

    /*
     * Command row
     */
    NFrameContainer *cmdFrame = new NFrameContainer(this);
    NGridContainer *cmdGrid = new NGridContainer();
    cmdGrid->setColumnStretch(0,1);
    cmdGrid->setColumnStretch(1,0);
    cmdFrame->setLayout(cmdGrid);

    QPushButton *cmdButton = new QPushButton(this);
    cmdButton->setIcon(QIcon(":/icons/system-search.png"));
    QObject::connect(
                cmdButton, SIGNAL(clicked(bool)),
                this, SLOT(handleSearchExe()));

    cmdGrid->addWidget(this->cmd, 0,0);
    cmdGrid->addWidget(cmdButton, 0,1);
    form->addRow("Executable", cmdFrame);
    // Command row END

    form->addRow("Arguments:", this->args);

    /*
     * Button box
     */
    QDialogButtonBox *buttonBox = new QDialogButtonBox(this);
    buttonBox->addButton(QDialogButtonBox::Cancel);
    buttonBox->addButton(QDialogButtonBox::Apply);
    QPushButton *cancel = buttonBox->button(QDialogButtonBox::Cancel);
    this->apply = buttonBox->button(QDialogButtonBox::Apply);
    this->apply->setDisabled(true);

    QObject::connect(
                cancel, SIGNAL(clicked(bool)),
                this, SLOT(reject()));
    QObject::connect(
                this->apply, SIGNAL(clicked(bool)),
                this, SLOT(accept()));


    QLabel *header = new QLabel(this);
    header->setText("Edit action configuration");

    grid->addWidget(header, 0,0);
    grid->addWidget(fr, 1,0);
    grid->addWidget(buttonBox, 2,0);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);
    grid->setRowStretch(2,0);
}

void MonitorActionCreate::handleSearchExe()
{
    QFileDialog fdiag(this);
    fdiag.setFileMode(QFileDialog::ExistingFile);
    // TODO filter only executables on linux?
    //fdiag.setFilter(QDir::AllDirs | QDir::Files | QDir::Executable);
    if (fdiag.exec()) {
        this->cmd->setText(fdiag.selectedFiles().at(0));
    }
}

void MonitorActionCreate::handleEditOk()
{
    if (this->name->text() == "") {
        this->apply->setDisabled(true);
        return;
    }

    if (this->cmd->text() == "") {
        this->apply->setDisabled(true);
        return;
    }

    this->apply->setDisabled(false);
}
