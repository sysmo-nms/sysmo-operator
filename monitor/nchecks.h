#ifndef NCHECKS_H
#define NCHECKS_H

#include "network/supercast.h"
#include "network/supercastsignal.h"

#include <QObject>
#include <QString>
#include <QJsonObject>
#include <QDebug>

class NChecks : public QObject
{
    Q_OBJECT

public:
    explicit NChecks(QObject *parent = 0);

signals:

public slots:
    void handleNetworkReply(QJsonObject obj);
};

#endif // NCHECKS_H
