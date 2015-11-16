#include "include/dialogs/newprobe.h"

NewProbe::NewProbe(QString forTarget, QWidget* parent) : QWizard(parent)
{
    this->setWindowTitle("New probe");
    this->setModal(true);
    this->setButtonText(QWizard::FinishButton, "Validate");
    this->setButtonText(QWizard::CancelButton, "Close");
    this->setWizardStyle(QWizard::ModernStyle);
    this->setMinimumWidth(800);
    this->setMinimumHeight(600);

    NewProbePage1* page1 = new NewProbePage1(forTarget, this);
    NewProbePage2* page2 = new NewProbePage2(forTarget, this);
    // TODO Simulate check
    //NewProbePage3* page3 = new NewProbePage3(this);
    this->setPage(1, page1);
    this->setPage(2, page2);
    //this->setPage(3, page3);
    this->setStartId(1);
}
