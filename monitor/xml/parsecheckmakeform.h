#ifndef PARSECHECKMAKEFORM_H
#define PARSECHECKMAKEFORM_H

#include <QXmlDefaultHandler>

#include <QDebug>


class ParseCheckMakeForm : public QXmlDefaultHandler
{
public:
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

#endif // PARSECHECKMAKEFORM_H
