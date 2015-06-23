#include "newprobepage2.h"

NewProbePage2::NewProbePage2(QWidget* parent) : QWizardPage(parent)
{
    this->setSubTitle("Complete the form to configure the new probe");
    this->setFinalPage(true);
    NGrid* grid = new NGrid();
    this->setLayout(grid);

    this->docs = new QTextEdit(this);
    this->docs->setReadOnly(true);
    grid->addWidget(this->docs);
}

void NewProbePage2::initializePage()
{
    QString str("Configure probe %1");
    QString probe_name(this->field("selection").toString());
    this->setTitle(str.arg(probe_name));


    QXmlSimpleReader reader;

    /*
     * Generate documentation
     */
    QXmlInputSource* doc_input = new QXmlInputSource();
    doc_input->setData(NChecks::getCheck(probe_name));
    ParseCheckMakeDoc*  doc_parser = new ParseCheckMakeDoc();
    reader.setContentHandler(doc_parser);
    reader.setErrorHandler(doc_parser);
    reader.parse(doc_input);
    this->docs->setHtml(doc_parser->doc);
    delete doc_parser;
    delete doc_input;


    /*
     * Generate form
     */
    QXmlInputSource* form_input = new QXmlInputSource();
    form_input->setData(NChecks::getCheck(probe_name));
    ParseCheckMakeForm* form_parser = new ParseCheckMakeForm();
    reader.setContentHandler(form_parser);
    reader.setErrorHandler(form_parser);
    reader.parse(form_input);
    delete form_parser;
    delete form_input;
}

bool NewProbePage2::isComplete() const
{
    return false;
}







