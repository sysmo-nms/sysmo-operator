#ifndef PARSECHECKMAKEGRAPHCMD_H
#define PARSECHECKMAKEGRAPHCMD_H

#include <QXmlDefaultHandler>
#include <QVariant>
#include <QMap>

#include <QDebug>

class ParseCheckMakeGraphCMD : public QXmlDefaultHandler
{

private:
    QMap<QString,QVariant> graphs;
    QMap<QString,QVariant> current_graph;
    QString     current_graph_id;
    QList<QVariant> current_draws;
    QMap<QString,QVariant> current_draw;
    QString     char_element;
    QString     prop_prefix;
    QString     prop_suffix;


public:
    bool startDocument();
    bool startElement(
            const QString        &namespaceURI,
            const QString        &localName,
            const QString        &qName,
            const QXmlAttributes &atts);
    bool endElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName);
    bool endDocument();
    bool characters(const QString &ch);
    QMap<QString,QVariant> config;
};

#endif // PARSECHECKMAKEGRAPHCMD_H
