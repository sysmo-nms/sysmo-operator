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
#include "include/monitor/menuprobe.h"

MenuProbe::MenuProbe(QWidget* parent) : QMenu(parent)
{
    this->probe_name = "undefined";


    /* TODO
    QAction* pause = new QAction("Pause/start probe", this);
    this->addAction(pause);
    QObject::connect(
                pause, SIGNAL(triggered(bool)),
                this,  SLOT(handlePauseProbe()));

    */
    //this->addSeparator();

    QAction* perfs = new QAction("Performances...", this);
    perfs->setIcon(QIcon(":/icons/utilities-system-monitor.png"));
    this->addAction(perfs);

    QObject::connect(
                perfs, SIGNAL(triggered(bool)),
                this, SLOT(handleShowPerf()));

    QAction* force = new QAction("Force check", this);
    force->setIcon(QIcon(":/icons/force.png"));
    this->addAction(force);
    QObject::connect(
                force, SIGNAL(triggered(bool)),
                this,  SLOT(handleForceProbe()));


    this->addSeparator();

    QAction* delete_probe = new QAction("Delete this probe", this);
    delete_probe->setIcon(QIcon(":/icons/process-stop.png"));
    this->addAction(delete_probe);
    QObject::connect(
                delete_probe, SIGNAL(triggered(bool)),
                this,         SLOT(handleDeleteProbe()));
}

void MenuProbe::handleShowPerf()
{
    ProbeWindow::openWindow(this->probe_name);
}

void MenuProbe::showMenuFor(QString probe, QPoint at)
{
    qDebug() << "show menu for probe" << probe << at;
    this->probe_name = probe;
    at.setX(at.x() + 12);
    this->popup(at);
}

void MenuProbe::handleForceProbe()
{
    qDebug() << "force probe" << this->probe_name;
    QMap<QString,QVariant> force_msg;
    QMap<QString,QVariant> value;
    value.insert("name", this->probe_name);
    force_msg.insert("from", "monitor");
    force_msg.insert("type", "forceProbeQuery");
    force_msg.insert("value", value);

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QVariant)),
                this, SLOT(handleForceProbeReply(QVariant)));
    Supercast::sendQuery(force_msg, sig);
}

void MenuProbe::handleForceProbeReply(QVariant reply_variant)
{
    qDebug() << "force probe reply" << reply_variant;
}

void MenuProbe::handleDeleteProbe()
{
    qDebug() << "delete probe" << this->probe_name;

    MessageBox* box = new MessageBox((QWidget *) this->parent());
    box->setIconType(Sysmo::MESSAGE_WARNING);
    box->setModal(true);
    box->setText("This action will permanently delete this probe.");
    box->setInformativeText("Do you want to continue?");
    box->setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    box->setDefaultButton(QMessageBox::No);
    int ret = box->exec();
    if (ret == QMessageBox::No) return;

    QMap<QString,QVariant> delete_msg;
    QMap<QString,QVariant> value;
    value.insert("name", this->probe_name);
    delete_msg.insert("from", "monitor");
    delete_msg.insert("type", "deleteProbeQuery");
    delete_msg.insert("value", value);

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QVariant)),
                this, SLOT(handleDeleteProbeReply(QVariant)));
    Supercast::sendQuery(delete_msg, sig);
}

void MenuProbe::handleDeleteProbeReply(QVariant reply)
{
    Q_UNUSED(reply);
    qDebug() << "delete probe" << this->probe_name;
}

void MenuProbe::handlePauseProbe()
{
    qDebug() << "pause probe" << this->probe_name;
}
