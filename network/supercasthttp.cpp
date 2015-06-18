#include "supercasthttp.h"

SupercastHTTP::~SupercastHTTP() {}

SupercastHTTP::SupercastHTTP(QObject* parent) : QNetworkAccessManager(parent)
{
    QObject::connect(
                this, SIGNAL(finished(QNetworkReply*)),
                this, SLOT(handleNetworkReply(QNetworkReply*)));
}

void SupercastHTTP::handleClientRequest(SupercastHttpRequest request)
{
    QNetworkRequest net_request = QNetworkRequest(QUrl(request.url));
    net_request.setAttribute(QNetworkRequest::User, QVariant(request.id));
    net_request.setAttribute(QNetworkRequest::HttpPipeliningAllowedAttribute, true);
    this->get(net_request);
}

void SupercastHTTP::handleNetworkReply(QNetworkReply* net_reply)
{
    int request_id   = net_reply->request().attribute(QNetworkRequest::User).toInt();
    QString            reply_body(net_reply->readAll());
    SupercastHttpReply reply(request_id, reply_body);
    net_reply->deleteLater();
    emit this->serverReply(reply);
}
