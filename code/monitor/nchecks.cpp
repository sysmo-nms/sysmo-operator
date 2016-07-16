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
#include "nchecks.h"

NChecks* NChecks::singleton = NULL;


QList<QString> NChecks::getCheckList() {

    return NChecks::singleton->checks->keys();

}


QString NChecks::getCheck(QString check) {

    return NChecks::singleton->checks->value(check);

}


NChecks::~NChecks() {delete this->checks;}


NChecks::NChecks(QObject *parent) : QObject(parent)
{

    NChecks::singleton = this;
    this->checks = new QHash<QString, QString>();
    QObject::connect(
                Supercast::getInstance(), SIGNAL(connectionStatus(int)),
                this,                     SLOT(connectionStatus(int)));

}


void NChecks::connectionStatus(int status)
{

    if (status != Supercast::CONNECTION_SUCCESS) return;

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QString)),
                this, SLOT(handleAllChecksReply(QString)));

    Supercast::httpGet("/nchecks/NChecksRepository.xml", sig);

}

void NChecks::handleAllChecksReply(QString body)
{

    QXmlInputSource* input = new QXmlInputSource();
    input->setData(body);

    ParseAllChecks* parser = new ParseAllChecks();

    QXmlSimpleReader reader;
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);

    QList<QString>* result = parser->getValue();

    QList<QString>::iterator it;
    for (
         it  = result->begin();
         it != result->end();
         ++it)
    {
        SupercastSignal* sig = new SupercastSignal();
        QObject::connect(
                    sig,  SIGNAL(serverMessage(QString)),
                    this, SLOT(handleCheckDefDeply(QString)));

        QString path = "/nchecks/%1";
        Supercast::httpGet(path.arg(*it), sig);
    }

    delete parser;
    delete input;

}


void NChecks::handleCheckDefDeply(QString body)
{

    ParseCheckGetId* parser = new ParseCheckGetId();
    QXmlInputSource* input  = new QXmlInputSource();
    QXmlSimpleReader reader;

    input->setData(body);
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);

    this->checks->insert(parser->getValue(), body);

    delete parser;
    delete input;
   
}








