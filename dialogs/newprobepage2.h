#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H

#include "nframe.h"
#include "nframecontainer.h"
#include "ngrid.h"
#include "ngridcontainer.h"
#include "monitor/monitor.h"
#include "monitor/nchecks.h"
#include "monitor/xml/parsecheckmakedoc.h"
#include "monitor/xml/parsecheckmakeform.h"
#include "dialogs/newprobeprogressdialog.h"

#include <QWidget>
#include <QFormLayout>
#include <QPushButton>
#include <QJsonObject>
#include <QList>
#include <QWizard>
#include <QWizardPage>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QTextEdit>
#include <QHash>

#include <QDebug>

class NewProbePage2 : public QWizardPage
{
public:
    NewProbePage2(QString forTarget, QWizard* parent = 0);
    void initializePage();
    void cleanupPage();
    bool validatePage();
    bool isComplete() const;
    int nextId() const;

private:
    QString     target     = "";
    QString     probe_class = "";
    QHash<QString,QLineEdit*>* args = NULL;
    QTextEdit*  docs       = NULL;
    NFrame*     form_frame = NULL;
    NGrid*      grid       = NULL;
};


#endif // NEWPROBEPAGE2_H
