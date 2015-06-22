#include "newprobepage2.h"

NewProbePage2::NewProbePage2(QWidget* parent) : QWizardPage(parent)
{
    this->setSubTitle("Complete the form to configure the new probe");
    this->setFinalPage(true);
}

void NewProbePage2::initializePage()
{
    QString str("Configure probe %1");
    QString probe_name(this->field("selection").toString());
    this->setTitle(str.arg(probe_name));
    QXmlInputSource* input = new QXmlInputSource();
    QXmlSimpleReader reader;
    CheckUIBuilder*  parser = new CheckUIBuilder(this);
    input->setData(NChecks::getCheck(probe_name));
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);
    delete input;
    delete parser;
}

bool NewProbePage2::isComplete() const
{
    return false;
}


CheckUIBuilder::CheckUIBuilder(QWidget *parent) : QXmlDefaultHandler()
{
    this->caller = parent;
}

bool CheckUIBuilder::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Check") {
        qDebug() << "id is: " << atts.value("Id");
        qDebug() << "up is: " << atts.value("UpdatesUrl");
        qDebug() << "type is: " << atts.value("Type");
        qDebug() << "class is: " << atts.value("Class");
    }
    if (qName== "Description") this->char_type = "Description";
    if (qName == "Flag") {
        qDebug() << "flag is: " << atts.value("Id");
        return true;
    }
    return true;
}

bool CheckUIBuilder::endElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Description") this->char_type = "";
    return true;
}

bool CheckUIBuilder::characters(const QString &ch)
{
    if (this->char_type == "Description") {
        qDebug() << "desc: " << ch;
    }
    return true;
}
