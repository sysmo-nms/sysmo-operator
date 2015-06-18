#ifndef SUPERCASTHTTP_H
#define SUPERCASTHTTP_H

#include "network/supercasthttpreply.h"
#include "network/supercasthttprequest.h"

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QUrl>
#include <QString>
#include <QVariant>
#include <QHash>

#include <QDebug>

class SupercastHTTP : public QNetworkAccessManager
{
    Q_OBJECT

public:
    explicit SupercastHTTP(QObject* parent = 0);
    ~SupercastHTTP();

public slots:
    void handleClientRequest(SupercastHttpRequest request);

private slots:
    void handleNetworkReply(QNetworkReply* reply);

signals:
    void serverReply(SupercastHttpReply reply);
};

#endif // SUPERCASTHTTP_H
