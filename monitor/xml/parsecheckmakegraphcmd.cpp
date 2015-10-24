#include "parsecheckmakegraphcmd.h"

bool ParseCheckMakeGraphCMD::startDocument() {
    this->char_element = "undefined";
    this->prop_prefix = "undefined";
    this->prop_suffix = "unefined";
    return true;
}
bool ParseCheckMakeGraphCMD::endDocument()   {return true;}

bool ParseCheckMakeGraphCMD::startElement(
        const QString        &namespaceURI,
        const QString        &localName,
        const QString        &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Performances") {
        this->config.insert("type",   QJsonValue(atts.value("Type")));
        return true;
    }

    if (qName == "Graph") {
        this->current_graph_id = atts.value("Id");
        this->current_graph = QJsonObject();
        this->current_graph.insert("minimum", QJsonValue(atts.value("Minimum")));
        this->current_graph.insert("maximum", QJsonValue(atts.value("Maximum")));
        this->current_graph.insert("rigid",   QJsonValue(atts.value("Rigid")));
        this->current_graph.insert("base",    QJsonValue(atts.value("Base")));
        this->current_graph.insert("unit",    QJsonValue(atts.value("Unit")));
        this->current_graph.insert("unitExponent",
                                      QJsonValue(atts.value("UnitExponent")));
        this->current_draws = QJsonArray();
        return true;
    }

    // Graph -> Title
    if (qName == "Title") {
        this->char_element = "title";
        return true;
    }
    // Graph -> VerticalLabel
    if (qName == "VerticalLabel") {
        this->char_element = "verticalLabel";
        return true;
    }
    // Graph -> Draw
    if (qName == "Draw") {
        this->current_draw = QJsonObject();
        this->current_draw.insert("type",
                                  QJsonValue(atts.value("Type")));
        this->current_draw.insert("color",
                                  QJsonValue(atts.value("Color")));
        this->current_draw.insert("dataSource",
                                  QJsonValue(atts.value("DataSource")));
        this->current_draw.insert("consolidation",
                                  QJsonValue(atts.value("Consolidation")));
        this->current_draw.insert("calculation",
                                  QJsonValue(atts.value("Calculation")));

        this->current_draw.insert("legend", QJsonValue("none"));
        this->char_element = "draw";
    }
    // PropertyPrefix
    if (qName == "PropertyPrefix") {
        this->char_element = "propertyPrefix";
        return true;
    }
    // PropertySuffix
    if (qName == "PropertySuffix") {
        this->char_element = "propertySuffix";
        return true;
    }
    return true;
}

bool ParseCheckMakeGraphCMD::endElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "PropertySuffix") {
        this->char_element = "undefined";
        return true;
    }
    if (qName == "PropertyPrefix") {
        this->char_element = "undefined";
        return true;
    }
    if (qName == "Title") {
        this->char_element = "undefined";
        return true;
    }
    if (qName == "VerticalLabel") {
        this->char_element = "undefined";
        return true;
    }
    if (qName == "Draw") {
        this->current_draws.append(QJsonValue(this->current_draw));
        this->char_element = "undefined";
        return true;
    }
    if (qName == "Graph") {
        this->current_graph.insert("draws", QJsonValue(this->current_draws));
        this->graphs.insert(this->current_graph_id, this->current_graph);
        return true;
    }
    if (qName == "GraphTable") {
        this->config.insert("graphs", QJsonValue(this->graphs));
        return true;
    }
    return true;
}

bool ParseCheckMakeGraphCMD::characters(const QString &ch)
{
    if (this->char_element == "undefined") return true;
    if (this->char_element == "propertySuffix") {
        this->config.insert("propertySuffix", QJsonValue(ch.simplified()));
        return true;
    }
    if (this->char_element == "propertyPrefix") {
        this->config.insert("propertyPrefix", QJsonValue(ch.simplified()));
        return true;
    }
    if (this->char_element == "title") {
        this->current_graph.insert("title", QJsonValue(ch.simplified()));
        return true;
    }
    if (this->char_element == "verticalLabel") {
        this->current_graph.insert("verticalLabel", QJsonValue(ch.simplified()));
        return true;
    }
    if (this->char_element == "draw") {
        this->current_draw.insert("legend", QJsonValue(ch.simplified()));
        return true;
    }
    qWarning() <<
         "parse graph xml nchecks unknown charcter read:" << this->char_element;
    return true;
}
