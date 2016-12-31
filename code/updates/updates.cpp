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

#include <QDebug>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QUrl>
#include <QTimer>
#include <QCoreApplication>

#include "updates/updates.h"
#include <md5.h>

/**
 * Try to connect to a sysmo.io service and find if a new version
 * of the client is available.
 */
Updates::Updates(QObject* parent)
    : QObject(parent)
{

    this->manager = new QNetworkAccessManager(this);
    QObject::connect(this->manager, SIGNAL(finished(QNetworkReply*)),
                     this,          SLOT(handleHttpReply(QNetworkReply*)));

    QTimer *timer = new QTimer(this);
    timer->setInterval(1000 * 300); // 5 minutes

    QObject::connect(timer, SIGNAL(timeout()),
                     this,  SLOT (check()));

    timer->start();
    QObject::connect(
                qApp, SIGNAL(aboutToQuit()),
                this, SLOT(deleteLater()));

}

void
Updates::check()
{
    MD5Context md5_context;
    MD5Init(&md5_context);

    // our file content
    manager->get(QNetworkRequest(QUrl("http://www.sysmo.io/releases.xml")));
    // TODO check PGP signature with what (Linux/Windows/Macos)
    //manager->get(QNetworkRequest(QUrl("http://www.sysmo.io/releases.xml.asc")));

    // Define the link to the release binary and download it:
    //manager->get(QNetworkRequest(QUrl("http://www.sysmo.io/myreleases.exe")));
    // TODO verify MD5 and SHA sums then (QCryptographicHash)
    // this->updateAvailable("hello crypto world");
}

void
Updates::handleHttpReply(QNetworkReply *reply)
{
    qDebug() << "REPLY got reply" << reply->readAll();
}
