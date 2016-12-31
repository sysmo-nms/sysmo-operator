/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
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
        this->config.clear();
        this->config.insert("type",   atts.value("Type"));
        return true;
    }

    if (qName == "Graph") {
        this->current_graph.clear();
        this->current_draws.clear();
        this->current_graph_id = atts.value("Id");
        this->current_graph.insert("minimum", atts.value("Minimum"));
        this->current_graph.insert("maximum", atts.value("Maximum"));
        this->current_graph.insert("rigid",   atts.value("Rigid"));
        this->current_graph.insert("base",    atts.value("Base"));
        this->current_graph.insert("unit",    atts.value("Unit"));
        this->current_graph.insert("unitExponent",
                                      atts.value("UnitExponent"));
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
        this->current_draw.clear();
        this->current_draw.insert("type",
                                  atts.value("Type"));
        this->current_draw.insert("color",
                                  atts.value("Color"));
        this->current_draw.insert("dataSource",
                                  atts.value("DataSource"));
        this->current_draw.insert("consolidation",
                                  atts.value("Consolidation"));
        this->current_draw.insert("calculation",
                                  atts.value("Calculation"));

        this->current_draw.insert("legend", "none");
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
        this->current_draws.append(this->current_draw);
        this->char_element = "undefined";
        return true;
    }
    if (qName == "Graph") {
        this->current_graph.insert("draws", this->current_draws);
        this->graphs.insert(this->current_graph_id, this->current_graph);
        return true;
    }
    if (qName == "GraphTable") {
        this->config.insert("graphs", this->graphs);
        return true;
    }
    return true;
}

bool ParseCheckMakeGraphCMD::characters(const QString &ch)
{
    if (this->char_element == "undefined") return true;
    if (this->char_element == "propertySuffix") {
        this->config.insert("propertySuffix", ch.simplified());
        return true;
    }
    if (this->char_element == "propertyPrefix") {
        this->config.insert("propertyPrefix", ch.simplified());
        return true;
    }
    if (this->char_element == "title") {
        this->current_graph.insert("title", ch.simplified());
        return true;
    }
    if (this->char_element == "verticalLabel") {
        this->current_graph.insert("verticalLabel", ch.simplified());
        return true;
    }
    if (this->char_element == "draw") {
        this->current_draw.insert("legend", ch.simplified());
        return true;
    }
    qWarning() <<
         "parse graph xml nchecks unknown charcter read:" << this->char_element;
    return true;
}
