#include "parsecheckmakeform.h"

ParseCheckMakeForm::~ParseCheckMakeForm() {
    delete this->mandatory;
    delete this->options;
}

bool ParseCheckMakeForm::startDocument()
{
    this->probe_class = "";
    this->current_flag = "";
    this->hint = "";
    this->helper_descr = "";
    this->helper_class = "";
    this->defaults = "";
    this->has_helper = false;
    this->is_hint = false;
    this->is_defaults = false;
    this->is_mandatory = true;

    this->mandatory = new QList<FormConfig>();
    this->options   = new QList<FormConfig>();
    return true;
}

bool ParseCheckMakeForm::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Check") {
        this->probe_class = atts.value("Class");
    }
    if (qName == "Flag") {
        this->current_flag = atts.value("Id");
    } else if (qName == "Hint") {
        this->is_hint = true;
    } else if (qName == "Default") {
        this->is_defaults  = true;
        this->is_mandatory = false;
    } else if (qName == "Helper") {
        this->has_helper = true;
        this->helper_class = atts.value("Class");
        this->helper_descr = atts.value("Descr");
    }
    return true;
}

bool ParseCheckMakeForm::endElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Flag") {

        FormConfig f;
        f.flag_name    = this->current_flag;
        f.hint         = this->hint;
        f.has_helper   = this->has_helper;
        f.helper_class = this->helper_class;
        f.helper_descr = this->helper_descr;
        f.defaults     = this->defaults;

        if (this->is_mandatory) {
            this->mandatory->append(f);
        } else {
            this->options->append(f);
        }

        /*
         * Reset to defaults
         */
        this->current_flag = "";
        this->hint         = "";
        this->is_mandatory = true;
        this->has_helper   = false;
        this->helper_class = "";
        this->helper_descr = "";
        this->defaults     = "";
    } else if (qName == "Hint") {
        this->is_hint = false;
    } else if (qName == "Default") {
        this->is_defaults = false;
    }
    return true;
}


bool ParseCheckMakeForm::characters(const QString &ch)
{
    if (this->is_hint) {
        this->hint.append(ch);
    } else if (this->is_defaults) {
        this->defaults.append(ch);
    }
    return true;
}

bool ParseCheckMakeForm::endDocument()
{
    return true;
}


FormConfig::FormConfig()
{
    this->flag_name = "";
    this->hint = "";
    this->defaults = "";
    this->has_helper = false;
    this->helper_descr = "";
    this->helper_class = "";
}

FormConfig::~FormConfig()
{

}

QString FormConfig::getFlagName()
{
    return this->flag_name;
}

FormConfig::FormConfig(FormConfig* other)
{
    this->flag_name = other->flag_name;
    this->hint = other->hint;
    this->defaults = other->defaults;
    this->has_helper = other->has_helper;
    this->helper_descr = other->helper_descr;
    this->helper_class = other->helper_class;
}


