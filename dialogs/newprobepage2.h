#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H

#include "nframe.h"
#include "monitor/nchecks.h"

#include <QWidget>
#include <QWizardPage>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QXmlDefaultHandler>

#include <QDebug>

class NewProbePage2 : public QWizardPage
{
public:
    NewProbePage2(QWidget* parent = 0);
    void initializePage();
    bool isComplete() const;
};


class CheckUIBuilder: public QXmlDefaultHandler
{
public:
    CheckUIBuilder(QWidget* parent);
    QWidget* caller = NULL;
    NFrame*  frame  = NULL;
    QString* doc    = NULL;
    QString  char_type = "";
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);
    bool endElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName);
    bool characters(const QString &ch);
};

#endif // NEWPROBEPAGE2_H
