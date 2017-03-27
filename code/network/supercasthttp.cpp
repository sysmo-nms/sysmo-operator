/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
#include "supercasthttp.h"

#include <QHostAddress>
#include <QUrl>
#include <QString>
#include <QVariant>
#include <QHash>
#include <QFile>
#include <QMetaType>

QNetworkRequest::Attribute SupercastHTTP::att_request =
        static_cast<QNetworkRequest::Attribute> (QNetworkRequest::User + 1);

QNetworkRequest::Attribute SupercastHTTP::att_opaque =
        static_cast<QNetworkRequest::Attribute> (QNetworkRequest::User + 2);

QNetworkRequest::Attribute SupercastHTTP::att_dstfile =
        static_cast<QNetworkRequest::Attribute> (QNetworkRequest::User + 3);

SupercastHTTP::~SupercastHTTP() {
}

SupercastHTTP::SupercastHTTP(QObject* parent)
: QNetworkAccessManager(parent) {

    QObject::connect(
            this, SIGNAL(finished(QNetworkReply*)),
            this, SLOT(handleNetworkReply(QNetworkReply*)));
}

void SupercastHTTP::handleClientRequest(SupercastHttpRequest request) {

    QNetworkRequest net_request = QNetworkRequest(request.url);
    net_request.setAttribute(
            SupercastHTTP::att_request,
            QVariant(request.id));
    net_request.setAttribute(
            SupercastHTTP::att_opaque,
            QVariant(request.opaque));
    net_request.setAttribute(
            SupercastHTTP::att_dstfile,
            QVariant(request.dst_file));
    net_request.setAttribute(
            QNetworkRequest::HttpPipeliningAllowedAttribute,
            QVariant(true));
    this->get(net_request);

}

void SupercastHTTP::handleNetworkReply(QNetworkReply* net_reply) {

    int request_id = net_reply->request()
            .attribute(SupercastHTTP::att_request)
            .toInt();
    QString opaque = net_reply->request()
            .attribute(SupercastHTTP::att_opaque)
            .toString();
    QString dst_file = net_reply->request()
            .attribute(SupercastHTTP::att_dstfile)
            .toString();

    if (dst_file == "none") {
        QString reply_body(net_reply->readAll());
        SupercastHttpReply reply(request_id, reply_body);
        emit this->serverReply(reply);
    } else {
        QFile file(dst_file);
        file.open(QIODevice::ReadWrite);
        file.write(net_reply->readAll());
        file.close();

        if (opaque == "undefined") {
            SupercastHttpReply reply(request_id, dst_file);
            emit this->serverReply(reply);
        } else {
            SupercastHttpReply reply(request_id, opaque);
            emit this->serverReply(reply);
        }
    }
    net_reply->deleteLater();

}
