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
#ifndef PARSECHECKMAKEGRAPHCMD_H
#define PARSECHECKMAKEGRAPHCMD_H

#include <QXmlDefaultHandler>
#include <QVariant>
#include <QString>
#include <QList>
#include <QMap>
#include <QVariant>

class ParseCheckMakeGraphCMD : public QXmlDefaultHandler {
private:
    QMap<QString, QVariant> graphs;
    QMap<QString, QVariant> current_graph;
    QString current_graph_id;
    QList<QVariant> current_draws;
    QMap<QString, QVariant> current_draw;
    QString char_element;
    QString prop_prefix;
    QString prop_suffix;


public:
    bool startDocument();
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);
    bool endElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName);
    bool endDocument();
    bool characters(const QString &ch);
    QMap<QString, QVariant> config;
};

#endif // PARSECHECKMAKEGRAPHCMD_H
