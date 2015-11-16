#include "include/monitor/nchecks.h"

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

    Supercast::httpGet("/nchecks/AllChecks.xml", sig);
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







