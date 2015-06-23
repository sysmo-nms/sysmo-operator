#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H

#include "nframe.h"
#include "ngrid.h"
#include "monitor/nchecks.h"
#include "monitor/xml/parsecheckmakedoc.h"
#include "monitor/xml/parsecheckmakeform.h"

#include <QWidget>
#include <QWizardPage>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QTextEdit>

#include <QDebug>

class NewProbePage2 : public QWizardPage
{
public:
    NewProbePage2(QWidget* parent = 0);
    void initializePage();
    bool isComplete() const;

private:
    QTextEdit* docs = NULL;
};


#endif // NEWPROBEPAGE2_H
