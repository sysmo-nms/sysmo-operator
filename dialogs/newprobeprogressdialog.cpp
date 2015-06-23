#include "newprobeprogressdialog.h"

NewProbeProgressDialog::NewProbeProgressDialog(QWidget* parent)
        : QProgressDialog(parent)
{
    this->setModal(true);
    this->setLabelText("Applying probe configuration");
    this->setMinimum(0);
    this->setMaximum(0);
}

