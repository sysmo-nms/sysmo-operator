/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

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
#include "parsecheckgetinfos.h"

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
