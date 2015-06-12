#ifndef NEWPROBEPAGE1_H
#define NEWPROBEPAGE1_H

#include <QObject>
#include <QWidget>
#include <QWizardPage>

class NewProbePage1 : public QWizardPage
{
public:
    NewProbePage1(QWidget* parent = 0);
    bool isComplete() const;
};

#endif // NEWPROBEPAGE1_H
