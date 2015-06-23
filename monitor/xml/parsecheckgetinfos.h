#ifndef PARSECHECKGETINFOS_H
#define PARSECHECKGETINFOS_H

#include <QXmlDefaultHandler>

class ParseCheckGetInfos : public QXmlDefaultHandler
{
public:
    QString name    = "";
    QString require = "simple";
    QString desc    = "";
    QString parse_pos = "";
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

#endif // PARSECHECKGETINFOS_H
