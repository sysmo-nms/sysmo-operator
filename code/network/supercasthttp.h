/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef SUPERCASTHTTP_H
#define SUPERCASTHTTP_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>

#include "supercasthttpreply.h"
#include "supercasthttprequest.h"

class SupercastHTTP : public QNetworkAccessManager {
    Q_OBJECT

public:
    explicit SupercastHTTP(QObject* parent = 0);
    ~SupercastHTTP();

public slots:
    void handleClientRequest(SupercastHttpRequest request);

private slots:
    void handleNetworkReply(QNetworkReply* reply);

private:
    static QNetworkRequest::Attribute att_request;
    static QNetworkRequest::Attribute att_opaque;
    static QNetworkRequest::Attribute att_dstfile;

signals:
    void serverReply(SupercastHttpReply reply);
};

#endif // SUPERCASTHTTP_H
