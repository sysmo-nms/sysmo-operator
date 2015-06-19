#ifndef NCHECKS_H
#define NCHECKS_H

#include "network/supercast.h"
#include "network/supercastsignal.h"

#include <QObject>
#include <QString>
#include <QDebug>

class NChecks : public QObject
{
    Q_OBJECT

public:
    explicit NChecks(QObject *parent = 0);

private:
    QString server_url;

signals:

public slots:
    void handleAllChecksReply(QString body);
    void connectionStatus(int status);
};

#endif // NCHECKS_H
