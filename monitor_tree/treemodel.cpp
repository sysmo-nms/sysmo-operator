#include "treemodel.h"

TreeModel::TreeModel(QWidget* parent) : QStandardItemModel(parent)
{
    this->targets = new QHash<QString, TargetItem*>();
    this->probes  = new QHash<QString, ProbeItem*>();

    QStringList headers = (QStringList()
          << "Target/Probe"
          << "Type/Host"
          << "Progress"
          << "Status"
          << "State"
          << "Last return");
    this->setHorizontalHeaderLabels(headers);
    Monitor* monitor = Monitor::getInstance();
    QObject::connect(
                monitor, SIGNAL(infoProbe(QJsonObject)),
                this,	 SLOT(handleInfoProbe(QJsonObject)));
    QObject::connect(
                monitor, SIGNAL(infoTarget(QJsonObject)),
                this,	 SLOT(handleInfoTarget(QJsonObject)));
    QObject::connect(
                monitor, SIGNAL(deleteProbe(QJsonObject)),
                this,	 SLOT(handleDeleteProbe(QJsonObject)));
    QObject::connect(
                monitor, SIGNAL(deleteTarget(QJsonObject)),
                this,	 SLOT(handleDeleteTarget(QJsonObject)));
    QObject::connect(
                monitor, SIGNAL(probeReturn(QJsonObject)),
                this,	 SLOT(handleProbeReturn(QJsonObject)));
}


TreeModel::~TreeModel()
{
    delete this->targets;
    delete this->probes;
}


void TreeModel::handleInfoProbe(QJsonObject message)
{
    QString info_type = message.value("infoType").toString("undefined");
    if (info_type == "create") {
        ProbeItem*  probe  = new ProbeItem(message);
        this->probes->insert(probe->name, probe);

        TargetItem* target = this->targets->value(probe->belong_to);
        QList<QStandardItem*> row;
        row << probe << probe->r1 << probe->r2 << probe->r3 << probe->r4 << probe->r5;
        target->appendRow(row);
        target->updateIconStatus();
    } else if (info_type == "update") {

        QString probe_name = message.value("name").toString("undefined");
        ProbeItem* probe = this->probes->value(probe_name);
        probe->updateInfo(message);
    }

}


void TreeModel::handleInfoTarget(QJsonObject message)
{
    QString info_type = message.value("infoType").toString("undefined");
    if (info_type == "create") {
        TargetItem* target = new TargetItem(message);
        this->targets->insert(target->name, target);
        QList<QStandardItem*> row;
        row << target << target->r1;
        this->appendRow(row);

    } else if (info_type == "update") {
        QString     target_name = message.value("name").toString("undefined");
        TargetItem* target      = this->targets->value(target_name);
        target->updateInfo(message);
    }
}


void TreeModel::handleDeleteProbe(QJsonObject message)
{
    QString     probe_name = message.value("name").toString("undefined");
    ProbeItem*  probe      = this->probes->take(probe_name);
    TargetItem* target     = this->targets->value(probe->belong_to);
    target->removeRow(probe->row());
}


void TreeModel::handleDeleteTarget(QJsonObject message)
{
    QString     target_name = message.value("name").toString("undefined");
    TargetItem* target      = this->targets->take(target_name);
    this->removeRow(target->row());
}


void TreeModel::handleProbeReturn(QJsonObject message)
{
    std::cout << "TreeModel handle probe return" << std::endl;

}
