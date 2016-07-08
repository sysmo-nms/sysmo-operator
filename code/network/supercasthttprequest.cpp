/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

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
#include "supercasthttprequest.h"


SupercastHttpRequest::SupercastHttpRequest() {

    this->id  = 0;
    this->url = QUrl();
    this->dst_file = "none";
    this->opaque = "undefined";

}


SupercastHttpRequest::SupercastHttpRequest(
        int request_id, QString dst, QUrl request_url)
{

    this->id       = request_id;
    this->url      = request_url;
    this->dst_file = dst;
    this->opaque = "undefined";

}


SupercastHttpRequest::SupercastHttpRequest(
        int request_id, QString dst, QUrl request_url, QString opaque_data)
{

    this->id       = request_id;
    this->url      = request_url;
    this->dst_file = dst;
    this->opaque   = opaque_data;

}


SupercastHttpRequest::SupercastHttpRequest(int request_id, QUrl request_url)
{

    this->id  = request_id;
    this->url = request_url;
    this->dst_file = "none";
    this->opaque = "undefined";

}
