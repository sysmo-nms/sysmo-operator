#include "nchecks.h"

NChecks* NChecks::singleton = NULL;

QList<QString> NChecks::getCheckList() {
    return NChecks::singleton->checks->keys();
}
QString        NChecks::getCheck(QString check) {
    return NChecks::singleton->checks->value(check);
}

NChecks::~NChecks() {delete this->checks;}
NChecks::NChecks(QObject *parent) : QObject(parent)
{
    NChecks::singleton = this;
    this->checks = new QHash<QString, QString>();
    QObject::connect(
                Supercast::getInstance(), SIGNAL(connectionStatus(int)),
                this, SLOT(connectionStatus(int)));
}


void NChecks::connectionStatus(int status)
{

    if (status != Supercast::ConnectionSuccess) return;

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QString)),
                this, SLOT(handleAllChecksReply(QString)));
    Supercast::httpGet("/nchecks/AllChecks.xml", sig);
}

void NChecks::handleAllChecksReply(QString body)
{

    QXmlInputSource* input = new QXmlInputSource();
    input->setData(body);

    AllChecksParser* parser = new AllChecksParser();

    QXmlSimpleReader reader;
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);
    QList<QString>::iterator it;
    for (
         it  = parser->values->begin();
         it != parser->values->end();
         ++it)
    {
        SupercastSignal* sig = new SupercastSignal();
        QObject::connect(
                    sig, SIGNAL(serverMessage(QString)),
                    this, SLOT(handleCheckDefDeply(QString)));
        QString path = "/nchecks/%1";
        Supercast::httpGet(path.arg(*it), sig);
    }

    delete parser;
    delete input;
}


void NChecks::handleCheckDefDeply(QString body)
{
    SimpleCheckParser* parser = new SimpleCheckParser();
    QXmlInputSource*   input  = new QXmlInputSource();
    input->setData(body);
    QXmlSimpleReader reader;
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);
    this->checks->insert(parser->name, body);
    delete parser;
    delete input;
}






/*
 * SimpleCheckParser
 */
bool SimpleCheckParser::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);

    if (qName == "Check")
    {
        this->name = atts.value("Id");
        return false;
    }
    return true;
}


/*
 * AllChecksParser
 */
AllChecksParser::~AllChecksParser() {delete this->values;}

bool AllChecksParser::startDocument()
{
    this->values = new QList<QString>();
    return true;
}

bool AllChecksParser::startElement(
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
