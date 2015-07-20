#include "supercasthttprequest.h"

SupercastHttpRequest::SupercastHttpRequest() {
    this->id  = 0;
    this->url = QUrl();
}

SupercastHttpRequest::SupercastHttpRequest(
        int request_id, QString dst, QUrl request_url)
{
    this->id  = request_id;
    this->url = request_url;
    this->dst_file = dst;
}


SupercastHttpRequest::SupercastHttpRequest(
        int request_id, QString dst, QUrl request_url, QString opaque_data)
{
    this->id  = request_id;
    this->url = request_url;
    this->dst_file = dst;
    this->opaque = opaque_data;
}

SupercastHttpRequest::SupercastHttpRequest(int request_id, QUrl request_url)
{
    this->id  = request_id;
    this->url = request_url;
}
