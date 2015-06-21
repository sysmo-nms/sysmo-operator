#include "newprobepage2.h"

NewProbePage2::NewProbePage2(QWidget* parent) : QWizardPage(parent)
{
    this->setSubTitle("Complete the form to configure the new probe");
    this->setFinalPage(true);
}

void NewProbePage2::initializePage()
{
    QString str("Configure probe %1");
    this->setTitle(str.arg(this->field("selection").toString()));
}

bool NewProbePage2::isComplete() const
{
    return false;
}
