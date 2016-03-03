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
#ifndef SUPERCASTHTTPREQUEST_H
#define SUPERCASTHTTPREQUEST_H

#include <QUrl>

class SupercastHttpRequest
{
public:
    /*
     * Default constructor for qRegisterMetaType?
     */
    SupercastHttpRequest();
    SupercastHttpRequest(
            int  request_id,
            QUrl request_url);
    SupercastHttpRequest(
            int     request_id,
            QString dst_file,
            QUrl    request_url);
    SupercastHttpRequest(
            int     request_id,
            QString dst_file,
            QUrl    request_url,
            QString opaque);

    int     id;
    QUrl    url;
    QString dst_file;
    QString   opaque;
};

#endif // SUPERCASTHTTPREQUEST_H
