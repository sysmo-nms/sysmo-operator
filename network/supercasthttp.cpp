#include "supercasthttp.h"

SupercastHTTP::~SupercastHTTP() {}

SupercastHTTP::SupercastHTTP(QObject* parent)
    : QNetworkAccessManager(parent)
{
    QObject::connect(
                this, SIGNAL(finished(QNetworkReply*)),
                this, SLOT(handleNetworkReply(QNetworkReply*)));
}

void SupercastHTTP::handleClientRequest(SupercastHttpRequest request)
{
    QNetworkRequest net_request = QNetworkRequest(request.url);
    net_request.setAttribute(
                QNetworkRequest::User,
                QVariant(request.id));
    net_request.setAttribute(
                QNetworkRequest::UserMax,
                QVariant(request.dst_file));
    net_request.setAttribute(
                QNetworkRequest::HttpPipeliningAllowedAttribute,
                QVariant(true));
    this->get(net_request);
}

void SupercastHTTP::handleNetworkReply(QNetworkReply* net_reply)
{
    int request_id   = net_reply->request()
                                        .attribute(QNetworkRequest::User)
                                        .toInt();
    QString dst_file = net_reply->request()
                                        .attribute(QNetworkRequest::UserMax)
                                        .toString();

    if (dst_file == "none") {
        QString            reply_body(net_reply->readAll());
        SupercastHttpReply reply(request_id, reply_body);
        emit this->serverReply(reply);
    } else {
        QFile file(dst_file);
        file.open(QIODevice::ReadWrite);
        file.write(net_reply->readAll());
        file.close();

        SupercastHttpReply reply(request_id, dst_file);
        emit this->serverReply(reply);
    }
    net_reply->deleteLater();
}
