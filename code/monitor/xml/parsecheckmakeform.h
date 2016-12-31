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
#ifndef PARSECHECKMAKEFORM_H
#define PARSECHECKMAKEFORM_H

#include <QXmlDefaultHandler>
#include <QList>

#include <QDebug>

class FormConfig
{
public:
    FormConfig(FormConfig* other);
    FormConfig();
    ~FormConfig();
    QString getFlagName();
    QString flag_name;
    QString hint;
    QString defaults;
    bool    has_helper;
    QString helper_descr;
    QString helper_class;
};


class ParseCheckMakeForm : public QXmlDefaultHandler
{
public:
    ParseCheckMakeForm();
    ~ParseCheckMakeForm();
    QList<FormConfig>* mandatory;
    QList<FormConfig>* options;
    QString probe_class;
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
    bool characters(const QString &ch);
    bool endDocument();

private:

    QString current_flag;
    QString hint;
    QString helper_descr;
    QString helper_class;
    QString defaults;

    bool    has_helper;
    bool    is_hint;
    bool    is_defaults;
    bool    is_mandatory;

};

#endif // PARSECHECKMAKEFORM_H
