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
#ifndef SOCKET_UTILS_H
#define SOCKET_UTILS_H

#include "socketutils.h"
#include "supercast.h"
#include <QAbstractSocket>
#include <QString>

namespace socketutils {

QString getErrorInfo(int status) {
    QString error_info;
    switch (status) {
    case Supercast::AUTHENTICATION_ERROR:
    {
        error_info = "Authentication failure.";
        break;
    }
    case QAbstractSocket::ConnectionRefusedError:
    {
        error_info = "The connection was refused by the peer.";
        break;
    }
    case QAbstractSocket::RemoteHostClosedError:
    {
        error_info = "The remote host closed the connection.";
        break;
    }
    case QAbstractSocket::HostNotFoundError:
    {
        error_info = "Host not found.";
        break;
    }
    case QAbstractSocket::SocketTimeoutError:
    {
        error_info = "Socket timed out.";
        break;
    }
    case QAbstractSocket::NetworkError:
    {
        error_info = "Network error.";
        break;
    }
    default:
    {
        error_info = "Unknown socket Error";
    }
    }
    return error_info;
}

QString getErrorString(int status) {
    QString error_text;
    switch (status) {
    case Supercast::AUTHENTICATION_ERROR:
    {
        error_text = "The authentication procedure has failed.";
        break;
    }
    case QAbstractSocket::ConnectionRefusedError:
    {
        error_text = "You may trying to connect to the wrong host, or the wrong port.";
        break;
    }
    case QAbstractSocket::RemoteHostClosedError:
    {
        error_text = "This can append if the host came down, or if the service is restarting.";
        break;
    }
    case QAbstractSocket::HostNotFoundError:
    {
        error_text = "Cannot resolve hostname.";
        break;
    }
    case QAbstractSocket::SocketTimeoutError:
    {
        error_text = "You may trying to connect to the wrong host, or the wrong port.";
        break;
    }
    case QAbstractSocket::NetworkError:
    {
        error_text = "Can not reach the host.";
        break;
    }
    default:
    {
        error_text = "";
    }
    }
    return error_text;

}

}
#endif // SOCKET_UTILS_H
