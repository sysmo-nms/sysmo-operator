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
    ProbeItem*  probe  = new ProbeItem(message);
    this->probes->insert(probe->name, probe);

    TargetItem* target = this->targets->value(probe->belong_to);
    QList<QStandardItem*> row;
    row << probe << probe->r1 << probe->r2 << probe->r3 << probe->r4 << probe->r5;
    target->appendRow(row);

}


void TreeModel::handleInfoTarget(QJsonObject message)
{
    TargetItem* target = new TargetItem(message);
    this->targets->insert(target->name, target);
    QList<QStandardItem*> row;
    row << target << target->r1;
    this->appendRow(row);
}


void TreeModel::handleDeleteProbe(QJsonObject message)
{
    std::cout << "TreeModel handle delete probe" << std::endl;

}


void TreeModel::handleDeleteTarget(QJsonObject message)
{
    std::cout << "TreeModel handle delete target" << std::endl;

}


void TreeModel::handleProbeReturn(QJsonObject message)
{
    std::cout << "TreeModel handle probe return" << std::endl;

}

QStandardItem* TreeModel::itemExist(QString name)
{
    return NULL;
}
