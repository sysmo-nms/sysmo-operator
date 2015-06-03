#include "treemodel.h"

TreeModel::TreeModel(QWidget* parent) : QStandardItemModel(parent)
{
    QStringList headers = (QStringList()
          << "Targets/Probes"
          << "Progress"
          << "Status"
          << "Step/Timeout"
          << "State"
          << "Host"
          << "Last return");
    this->setHorizontalHeaderLabels(headers);
}

