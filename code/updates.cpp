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

#include <QDebug>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QUrl>
#include <QTimer>
#include <QCoreApplication>

#include "updates.h"

Updates::Updates() : QObject(0) {
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

void Updates::start()
{
    /*
     * Will trigger a check for update every five minutes.
     */
    new Updates();
}

void Updates::check()
{
    manager->get(
      QNetworkRequest(
        QUrl("https://api.github.com/repos/sysmo-nms/sysmo-operator/releases")));

}

void Updates::handleHttpReply(QNetworkReply *reply)
{

    /* TODO handle json reply
     * If (update available)
     *  emit updateAvailable(msg)
     */

        qDebug() << "got reply" << reply;

}
