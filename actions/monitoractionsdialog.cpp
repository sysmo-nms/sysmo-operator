#include "monitoractionsdialog.h"

MonitorActionsDialog::MonitorActionsDialog(QWidget* parent, QString target)
    : QDialog(parent)
{

    new QLabel(target, this);

}
