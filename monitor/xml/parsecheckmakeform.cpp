#include "parsecheckmakeform.h"

bool ParseCheckMakeForm::startDocument()
{
    qDebug() << "start";
    return true;
}

bool ParseCheckMakeForm::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    Q_UNUSED(atts);
    qDebug() << "start element: " << qName;
    return true;
}

bool ParseCheckMakeForm::endElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    qDebug() << "end element: " << qName;
    return true;
}


bool ParseCheckMakeForm::characters(const QString &ch)
{
    Q_UNUSED(ch);
    return true;
}

bool ParseCheckMakeForm::endDocument()
{
    qDebug() << "end";
    return true;
}
