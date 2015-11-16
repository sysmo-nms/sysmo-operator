#ifndef PARSEALLCHECKS_H
#define PARSEALLCHECKS_H

#include <QXmlDefaultHandler>

class ParseAllChecks : public QXmlDefaultHandler
{
public:
    ~ParseAllChecks();
    bool startDocument();
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);
    QList<QString>* getValue();

private:
    QList<QString>* values;

};

#endif // PARSEALLCHECKS_H
