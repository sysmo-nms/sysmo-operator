#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H

#include <QWidget>
#include <QWizardPage>
#include <QDebug>

class NewProbePage2 : public QWizardPage
{
public:
    NewProbePage2(QWidget* parent = 0);
    void initializePage();
    bool isComplete() const;
};

#endif // NEWPROBEPAGE2_H
