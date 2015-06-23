#include "parsecheckgetid.h"

bool ParseCheckGetId::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);

    if (qName == "Check")
    {
        this->name = atts.value("Id");
        return false;
    }
    return true;
}

QString ParseCheckGetId::getValue()
{
    return this->name;
}
