#include "supercasthttprequest.h"

SupercastHttpRequest::SupercastHttpRequest() {
    this->id  = 0;
    this->url = QUrl();
}

SupercastHttpRequest::SupercastHttpRequest(int request_id, QUrl request_url)
{
    this->id  = request_id;
    this->url = request_url;
}
