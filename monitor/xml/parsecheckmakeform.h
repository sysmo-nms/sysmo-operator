#ifndef PARSECHECKMAKEFORM_H
#define PARSECHECKMAKEFORM_H

#include <QXmlDefaultHandler>

#include <QLineEdit>
#include <QList>

#include <QDebug>

class FormConfig
{
public:
    FormConfig(FormConfig* other);
    FormConfig();
    ~FormConfig();
    QString getFlagName();
    QString flag_name    = "";
    QString hint         = "";
    QString defaults     = "";
    bool    has_helper   = false;
    QString helper_id    = "";
    QString helper_class = "";
};


class ParseCheckMakeForm : public QXmlDefaultHandler
{
public:
    ~ParseCheckMakeForm();
    QList<FormConfig>* mandatory = NULL;
    QList<FormConfig>* options   = NULL;
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

    QString current_flag = "";
    QString hint         = "";
    QString helper_id    = "";
    QString helper_class = "";
    QString defaults     = "";

    bool    has_helper   = false;
    bool    is_hint      = false;
    bool    is_defaults  = false;
    bool    is_mandatory = true;

};

#endif // PARSECHECKMAKEFORM_H
