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

    /*
     * Generate documentation
     */
    QXmlInputSource* input = new QXmlInputSource();
    QXmlSimpleReader reader;
    ParseCheckMakeDoc*  parser = new ParseCheckMakeDoc();
    input->setData(NChecks::getCheck(probe_name));
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);
    this->docs->setHtml(parser->doc);
    delete input;
    delete parser;


    /*
     * Generate form
     */
}

bool NewProbePage2::isComplete() const
{
    return false;
}







