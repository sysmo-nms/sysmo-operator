#include "newtarget.h"

NewTarget::NewTarget(QWidget* parent) : QWizard(parent)
{
    this->setWindowTitle("New target");
    this->setModal(true);
    this->setOption(QWizard::NoBackButtonOnLastPage, true);
    this->setButtonText(QWizard::FinishButton, "Validate");
    this->setButtonText(QWizard::CancelButton, "Close");
    this->setWizardStyle(QWizard::ModernStyle);

    NewTargetPage1* page1 = new NewTargetPage1(this);
    this->setPage(1, page1);
    this->setStartId(1);
    this->setFixedWidth(525);
}
