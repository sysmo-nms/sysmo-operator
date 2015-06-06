#include "newtarget.h"

NewTarget::NewTarget(QWidget* parent) : QWizard(parent)
{
    this->hide();
    this->setWindowTitle("New target");
}
