#ifndef NCHECKS_H
#define NCHECKS_H

#include "network/supercast.h"
#include "network/supercastsignal.h"

#include <QObject>
#include <QString>
#include <QDebug>
#include <QXmlSimpleReader>
#include <QXmlDefaultHandler>
#include <QXmlInputSource>
#include <QList>

class NChecks : public QObject
{
    Q_OBJECT

public:
    explicit NChecks(QObject *parent = 0);
    ~NChecks();
    QList<QString> getCheckList();
    QString        getCheck(QString check);

private:
    QHash<QString, QString>* checks      = NULL;

signals:

public slots:
    void handleAllChecksReply(QString body);
    void handleCheckDefDeply(QString body);
    void connectionStatus(int status);
};


class AllChecksParser : public QXmlDefaultHandler
{
public:
    ~AllChecksParser();
    QList<QString>* values = NULL;
    bool startDocument();
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);
};


class SimpleCheckParser : public QXmlDefaultHandler
{
public:
    QString name;
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);

};

#endif // NCHECKS_H
