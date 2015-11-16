#include "include/monitor/xml/parsecheckgetinfos.h"

bool ParseCheckGetInfos::startDocument()
{
    this->name = "";
    this->require = "simple";
    this->desc = "";
    this->parse_pos = "";
    return true;
}

bool ParseCheckGetInfos::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Check") {
        this->name = atts.value("Id");
    } else if (qName == "Require") {
        this->require = atts.value("Ressource");
    } else if (qName == "Description") {
        this->parse_pos = "Description";
    }
    return true;
}

bool ParseCheckGetInfos::endElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Description") this->parse_pos = "";
    return true;
}

bool ParseCheckGetInfos::characters(const QString &ch)
{
    if (this->parse_pos == "Description") this->desc = ch;
    return true;
}
