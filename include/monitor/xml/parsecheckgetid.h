#ifndef PARSECHECKGETID_H
#define PARSECHECKGETID_H

#include <QXmlDefaultHandler>

class ParseCheckGetId : public QXmlDefaultHandler
{
public:
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);

    QString getValue();

private:
    QString name;
};

#endif // PARSECHECKGETID_H
