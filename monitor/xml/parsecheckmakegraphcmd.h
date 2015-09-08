#ifndef PARSECHECKMAKEGRAPHCMD_H
#define PARSECHECKMAKEGRAPHCMD_H

#include <QXmlDefaultHandler>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>

#include <QDebug>

class ParseCheckMakeGraphCMD : public QXmlDefaultHandler
{

private:
    QJsonObject graphs;
    QJsonObject current_graph;
    QString     current_graph_id;
    QJsonArray  current_draws;
    QJsonObject current_draw;
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
    QJsonObject config;
};

#endif // PARSECHECKMAKEGRAPHCMD_H
