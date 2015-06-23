#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H

#include "nframe.h"
#include "ngrid.h"
#include "monitor/nchecks.h"

#include <QWidget>
#include <QWizardPage>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QXmlDefaultHandler>
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


class CheckUIBuilder: public QXmlDefaultHandler
{
public:
    QString  doc       = "";
    QString  flags     = "";
    QString  char_type = "";
    bool startDocument();
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
    bool endDocument();
};

#endif // NEWPROBEPAGE2_H
