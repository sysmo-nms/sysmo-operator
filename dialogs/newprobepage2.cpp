#include "newprobepage2.h"

NewProbePage2::NewProbePage2(
        QString  forTarget,
        QWizard* parent) : QWizardPage(parent)
{
    this->target = forTarget;
    this->setSubTitle("Complete the form to configure the new probe");
    this->setFinalPage(true);
    this->grid = new NGrid();
    this->setLayout(grid);

    this->docs = new QTextEdit(this);
    this->docs->setReadOnly(true);
    this->grid->addWidget(this->docs, 0, 1);
    this->grid->setColumnStretch(0,1);
    this->grid->setColumnStretch(1,1);
}

int NewProbePage2::nextId() const
{
    return -1;
}

void NewProbePage2::cleanupPage()
{
    this->grid->removeWidget(this->form_frame);
    this->form_frame->deleteLater();
    delete this->args;
}

void NewProbePage2::initializePage()
{
    this->form_frame = new NFrame(this);
    this->grid->addWidget(this->form_frame, 0, 0);
    this->args = new QHash<QString, QLineEdit*>();

    QString str("Configure probe %1");
    QString probe_name(this->field("selection").toString());
    this->setTitle(str.arg(probe_name));

    QXmlSimpleReader reader;

    // TODO maybe use QDomDocument insteed

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

    this->probe_class = form_parser->probe_class;

    QFormLayout* form = new QFormLayout();
    this->form_frame->setLayout(form);

    QList<FormConfig>* mandat = form_parser->mandatory;
    QList<FormConfig>::iterator i;
    for (i = mandat->begin(); i != mandat->end(); ++i)
    {
        qDebug() << "iterate" << i->flag_name;
        QLineEdit* edit = new QLineEdit(this->form_frame);
        this->args->insert(i->flag_name, edit);
        edit->setPlaceholderText(i->hint);
        edit->setToolTip(i->hint);
        if (i->has_helper) {
            NFrameContainer* fr = new NFrameContainer(this->form_frame);
            NGridContainer*  gr = new NGridContainer(fr);
            QPushButton*     hbut = new QPushButton(this->form_frame);
            gr->addWidget(edit, 0,0);
            gr->addWidget(hbut, 0,1);
            gr->setColumnStretch(0,1);
            gr->setColumnStretch(1,0);
            form->addRow(i->flag_name, fr);
        } else {
            form->addRow(i->flag_name, edit);
        }
    }

    NFrame* separator = new NFrame(this->form_frame);
    separator->setFixedHeight(30);
    form->addRow(separator);

    QList<FormConfig>* options = form_parser->options;
    QList<FormConfig>::iterator j;
    for (j = options->begin(); j != options->end(); ++j)
    {
        qDebug() << "iterate" << j->flag_name;
        QLineEdit* edit = new QLineEdit(this->form_frame);
        this->args->insert(j->flag_name, edit);
        edit->setPlaceholderText(j->hint);
        edit->setText(j->defaults);
        edit->setToolTip(j->hint);
        if (j->has_helper) {
            NFrameContainer* fr = new NFrameContainer(this->form_frame);
            NGridContainer*  gr = new NGridContainer(fr);
            QPushButton*     hbut = new QPushButton(this->form_frame);
            gr->addWidget(edit, 0,0);
            gr->addWidget(hbut, 0,1);
            gr->setColumnStretch(0,1);
            gr->setColumnStretch(1,0);
            form->addRow(j->flag_name, fr);
        } else {
            form->addRow(j->flag_name, edit);
        }
    }

    delete form_parser;
    delete form_input;

    QLineEdit* host_edit = this->args->value("host");
    if (host_edit == NULL) return;

    QJsonObject val  = Monitor::getInstance()->targets->value(this->target);
    QString     host = val.value("properties").toObject().value("host").toString("");
    host_edit->setText(host);
}

bool NewProbePage2::validatePage()
{
    QString probe_name(this->field("selection").toString());
    NewProbeProgressDialog* dial = new NewProbeProgressDialog(
                this->args,
                this->target,
                probe_name,
                this->probe_class,
                this);
    QObject::connect(
                dial, SIGNAL(accepted()),
                this, SLOT(close()));
    QObject::connect(
                dial, SIGNAL(canceled()),
                this, SLOT(close()));
    QObject::connect(
                dial, SIGNAL(rejected()),
                this, SLOT(close()));

    dial->open();
    return false;
}

bool NewProbePage2::isComplete() const
{
    return true;
}
