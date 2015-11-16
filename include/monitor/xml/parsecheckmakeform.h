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
