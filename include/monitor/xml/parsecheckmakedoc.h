#ifndef PARSECHECKMAKEDOC_H
#define PARSECHECKMAKEDOC_H

#include <QXmlDefaultHandler>

#include <QDebug>

class ParseCheckMakeDoc : public QXmlDefaultHandler
{
public:
    QString  doc;
    QString  flags;
    QString  char_type;
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

#endif // PARSECHECKMAKEDOC_H
