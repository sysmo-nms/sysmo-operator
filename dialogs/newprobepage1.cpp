#include "newprobepage1.h"

NewProbePage1::NewProbePage1(QWidget* parent) : QWizardPage(parent)
{
    this->setTitle("Select a probe");
    this->setSubTitle("User this form to add a probe to the target");

}

bool NewProbePage1::isComplete() const
{
    return false;
}
