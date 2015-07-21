#ifndef NCHECKS_H
#define NCHECKS_H

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "monitor/xml/parseallchecks.h"
#include "monitor/xml/parsecheckgetid.h"

#include <QObject>
#include <QString>
#include <QDebug>
#include <QXmlSimpleReader>
#include <QXmlInputSource>
#include <QList>

class NChecks : public QObject
{
    Q_OBJECT

public:
    explicit NChecks(QObject *parent = 0);
    ~NChecks();
    static QList<QString> getCheckList();
    static QString        getCheck(QString check);

private:
    QHash<QString, QString>* checks = NULL;
    static NChecks* singleton;

signals:

public slots:
    void handleAllChecksReply(QString body);
    void handleCheckDefDeply(QString body);
    void connectionStatus(int status);
};

#endif // NCHECKS_H
