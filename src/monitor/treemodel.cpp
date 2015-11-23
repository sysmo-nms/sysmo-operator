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
#include "include/monitor/treemodel.h"

TreeModel::TreeModel(QWidget* parent) : QStandardItemModel(parent)
{
    this->targets = new QMap<QString, ItemTarget*>();
    this->probes  = new QMap<QString, ItemProbe*>();

    QStringList headers = (QStringList()
          << "Target/Probe"
          << "Status"
          << "State"
          << "Progress"
          << "Last return");
    this->setHorizontalHeaderLabels(headers);

    Monitor* monitor = Monitor::getInstance();
    QObject::connect(
                monitor, SIGNAL(infoProbe(QVariant)),
                this,	 SLOT(handleInfoProbe(QVariant)));
    QObject::connect(
                monitor, SIGNAL(infoTarget(QVariant)),
                this,	 SLOT(handleInfoTarget(QVariant)));
    QObject::connect(
                monitor, SIGNAL(deleteProbe(QVariant)),
                this,	 SLOT(handleDeleteProbe(QVariant)));
    QObject::connect(
                monitor, SIGNAL(deleteTarget(QVariant)),
                this,	 SLOT(handleDeleteTarget(QVariant)));
    QObject::connect(
                monitor, SIGNAL(probeReturn(QVariant)),
                this,	 SLOT(handleProbeReturn(QVariant)));
}


TreeModel::~TreeModel()
{
    delete this->targets;
    delete this->probes;
}

void TreeModel::handleInfoProbe(QVariant message_var)
{
    QMap<QString,QVariant> message = message_var.toMap();
    QString info_type = message.value("infoType").toString();

    if (info_type == "create") {

        ItemProbe*  probe = new ItemProbe(message);
        this->probes->insert(probe->name, probe);

        QList<QStandardItem*> row;
        row << probe << probe->item_status << probe->item_state
            << probe->item_progress << probe->item_last_return;

        ItemTarget* target = this->targets->value(probe->belong_to);
        QString filter = target->data(Sysmo::ROLE_FILTER_ORIG).toString();
        probe->setTargetFilter(filter);

        target->appendRow(row);
        target->updateIconStatus();
        target->updateProbeFilter(probe->name, message);
        emit this->selectIndex(probe->index());

    } else if (info_type == "update") {
        QString probe_name = message.value("name").toString();

        ItemProbe*  probe  = this->probes->value(probe_name);
        ItemTarget* target = this->targets->value(probe->belong_to);

        probe->updateInfo(message);
        target->updateProbeFilter(probe->name, message);
        target->updateIconStatus();
    }
}


void TreeModel::handleInfoTarget(QVariant message_var)
{
    QMap<QString,QVariant> message = message_var.toMap();
    QString info_type = message.value("infoType").toString();
    if (info_type == "create") {
        ItemTarget* target = new ItemTarget(message);
        this->targets->insert(target->name, target);
        this->appendRow(target);

        emit this->selectIndex(target->index());
        emit this->expandIndex(target->index());

    } else if (info_type == "update") {
        QString     target_name = message.value("name").toString();
        ItemTarget* target      = this->targets->value(target_name);
        target->updateInfo(message);
    }
}


void TreeModel::handleDeleteProbe(QVariant message_var)
{
    QMap<QString,QVariant> message = message_var.toMap();
    QString     probe_name = message.value("name").toString();
    ItemProbe*  probe      = this->probes->take(probe_name);
    ItemTarget* target     = this->targets->value(probe->belong_to);
    target->removeRow(probe->row());
    target->deleteProbeFilter(probe->name);
    target->updateIconStatus();
}


void TreeModel::handleDeleteTarget(QVariant message_var)
{
    QMap<QString,QVariant> message = message_var.toMap();
    QString     target_name = message.value("name").toString();
    ItemTarget* target      = this->targets->take(target_name);
    this->removeRow(target->row());
}


void TreeModel::handleProbeReturn(QVariant message_var)
{
    QMap<QString,QVariant> message = message_var.toMap();
    QString     probe_name = message.value("name").toString();
    ItemProbe*  probe      = this->probes->value(probe_name);
    probe->updateReturnInfo(message);
}
