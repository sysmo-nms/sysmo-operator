#include "monitoractionsdialog.h"

MonitorActionsDialog::MonitorActionsDialog(QWidget* parent, QString target)
    : QDialog(parent)
{
    NGrid* grid = new NGrid();
    this->setLayout(grid);

    new QLabel(target, this);
}
