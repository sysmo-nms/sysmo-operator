#include "treemodel.h"

TreeModel::TreeModel(QWidget* parent) : QStandardItemModel(parent)
{
    this->targets = new QHash<QString, ItemTarget*>();
    this->probes  = new QHash<QString, ItemProbe*>();

    QStringList headers = (QStringList()
          << "Target/Probe"
          << "Status"
          << "State"
          << "Progress"
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

    if (info_type == "create")
    {
        ItemProbe*  probe = new ItemProbe(message);
        this->probes->insert(probe->name, probe);


        QList<QStandardItem*> row;
        row << probe << probe->item_status << probe->item_state
            << probe->item_progress << probe->item_last_return;

        ItemTarget* target = this->targets->value(probe->belong_to);
        target->appendRow(row);
        target->updateIconStatus();

    }
    else if (info_type == "update")
    {
        QString probe_name = message.value("name").toString("undefined");

        ItemProbe*  probe  = this->probes->value(probe_name);
        ItemTarget* target = this->targets->value(probe->belong_to);

        probe->updateInfo(message);
        target->updateIconStatus();
    }
}


void TreeModel::handleInfoTarget(QJsonObject message)
{
    QString info_type = message.value("infoType").toString("undefined");
    if (info_type == "create")
    {
        ItemTarget* target = new ItemTarget(message);
        this->targets->insert(target->name, target);
        this->appendRow(target);

        emit this->expandIndex(target->index());
    }
    else if (info_type == "update")
    {
        QString     target_name = message.value("name").toString("undefined");
        ItemTarget* target      = this->targets->value(target_name);
        target->updateInfo(message);
    }
}


void TreeModel::handleDeleteProbe(QJsonObject message)
{
    QString     probe_name = message.value("name").toString("undefined");
    ItemProbe*  probe      = this->probes->take(probe_name);
    ItemTarget* target     = this->targets->value(probe->belong_to);
    target->removeRow(probe->row());
    target->updateIconStatus();
}


void TreeModel::handleDeleteTarget(QJsonObject message)
{
    QString     target_name = message.value("name").toString("undefined");
    ItemTarget* target      = this->targets->take(target_name);
    this->removeRow(target->row());
}


void TreeModel::handleProbeReturn(QJsonObject message)
{
    QString     probe_name = message.value("name").toString("undefined");
    ItemProbe*  probe      = this->probes->value(probe_name);
    probe->updateReturnInfo(message);
}
