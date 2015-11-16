#include "include/monitor/xml/parseallchecks.h"

ParseAllChecks::~ParseAllChecks() {delete this->values;}

bool ParseAllChecks::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);

    if (qName == "CheckUrl") {
        this->values->append(atts.value("Value"));
    }
    return true;
}

bool ParseAllChecks::startDocument()
{
    this->values = new QList<QString>();
    return true;
}

QList<QString>* ParseAllChecks::getValue()
{
    return this->values;
}
