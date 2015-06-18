#include "supercasthttprequest.h"

SupercastHttpRequest::SupercastHttpRequest() {
    this->id  = 0;
    this->url = "undefined";
}

SupercastHttpRequest::SupercastHttpRequest(int request_id, QString request_url)
{
    this->id  = request_id;
    this->url = request_url;
}
