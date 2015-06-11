#include "newprobe.h"

NewProbe::NewProbe(QWidget* parent) : QWizard(parent)
{
    this->hide();
    this->setWindowTitle("New probe");
    this->setModal(true);
    this->setOption(QWizard::NoBackButtonOnLastPage, true);
    this->setButtonText(QWizard::FinishButton, "Validate");
    this->setButtonText(QWizard::CancelButton, "Close");
    this->setWizardStyle(QWizard::ModernStyle);

    NewProbePage1* page1 = new NewProbePage1(this);
    this->setPage(1, page1);
    this->setStartId(1);
}

