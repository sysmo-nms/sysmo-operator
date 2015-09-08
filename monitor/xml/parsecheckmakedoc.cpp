#include "parsecheckmakedoc.h"

bool ParseCheckMakeDoc::startDocument()
{
    this->doc = "";
    this->flags = "";
    this->char_type = "";
    this->doc.append("<html><body>");
    this->flags.append("<h2>Options</h2><p><ul>");
    return true;
}



bool ParseCheckMakeDoc::endDocument()
{
    this->flags.append("</ul></p>");
    this->doc.append(this->flags);
    this->doc.append("</ul></p>");
    this->doc.append("</body></html>");
    return true;
}

bool ParseCheckMakeDoc::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Check") {
        QString doctpl;
        doctpl.append("<h1>%1</h1>")
                .append("<p><ul>")
                .append("<li><strong>Class:</strong> %2</li>")
                .append("<li><strong>Version:</strong> %3</li>");
        QString docstr = doctpl
                .arg(atts.value("Id"))
                .arg(atts.value("Class"))
                .arg(atts.value("Version"));
        qDebug() << docstr;
        this->doc.append(docstr);
        return true;
    }
    if (qName == "UpdatesUrl") {
        this->char_type = "UpdatesUrl";
        this->doc.append("<li><strong>Updates:</strong> ");
    }
    if (qName == "Author") {
        this->char_type = "Author";
        this->doc.append("<li><strong>Author:</Strong> ");
    }
    if (qName == "Description") {
        this->char_type = "Description";
        this->doc.append("<h2>Description</h2><p>");
        return true;
    }
    if (qName == "Overview") {
        this->char_type = "Overview";
        this->doc.append("<h2>Overview</h2><p>");
        return true;
    }
    if (qName == "GraphTable") {
        this->doc.append("<h2>Graphs</h2><p><ul>");
    }
    if (qName == "Graph") {
        QString g = "<li>%1</li>";
        this->doc.append(g.arg(atts.value("Id")));
    }
    if (qName == "Flag") {
        QString f = "<li><strong>%1</strong><ul>";
        this->flags.append(f.arg(atts.value("Id")));
        return true;
    }
    if (qName == "Default") {
        QString d = "<li>Default: ";
        this->flags.append(d);
        this->char_type = "Default";
    }
    if (qName == "Usage") {
        this->flags.append("<li>Usage: ");
        this->char_type = "Usage";
    }
    return true;
}

bool ParseCheckMakeDoc::endElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "UpdatesUrl") {
        this->char_type = "";
        this->doc.append("</li>");
    }
    if (qName == "Author") {
        this->char_type = "";
        this->doc.append("</li>");
    }
    if (qName == "Description") {
        this->char_type = "";
        this->doc.append("</p>");
    }
    if (qName == "Overview") {
        this->char_type = "";
        this->doc.append("</p>");
    }
    if (qName == "GraphTable") {
        this->char_type = "";
        this->doc.append("</ul></p>");
    }
    if (qName == "Flag") {
        this->char_type = "";
        this->flags.append("</ul></li>");
    }
    if (qName == "Default") {
        this->char_type = "";
        this->flags.append("</li>");
    }
    if (qName == "Usage") {
        this->char_type = "";
        this->flags.append("</li>");
    }

    return true;
}

bool ParseCheckMakeDoc::characters(const QString &ch)
{
    if (this->char_type == "UpdatesUrl") {
        this->doc.append(ch);
        return true;
    }
    if (this->char_type == "Author") {
        this->doc.append(ch);
        return true;
    }
    if (this->char_type == "Description") {
        this->doc.append(ch);
        return true;
    }
    if (this->char_type == "Overview") {
        this->doc.append(ch);
        return true;
    }
    if (this->char_type == "Default") {
        this->flags.append(ch);
    }
    if (this->char_type == "Usage") {
        this->flags.append(ch);
    }
    return true;
}
