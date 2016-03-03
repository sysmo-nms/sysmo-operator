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
#ifndef NCHECKS_H
#define NCHECKS_H

#include "../network/supercast.h"
#include "../network/supercastsignal.h"
#include "xml/parseallchecks.h"
#include "xml/parsecheckgetid.h"

#include <QObject>
#include <QString>
#include <QDebug>
#include <QXmlSimpleReader>
#include <QXmlInputSource>
#include <QList>

class NChecks : public QObject
{
    Q_OBJECT

public:
    explicit NChecks(QObject *parent = 0);
    ~NChecks();
    static QList<QString> getCheckList();
    static QString        getCheck(QString check);

private:
    QHash<QString, QString>* checks;
    static NChecks* singleton;

signals:

public slots:
    void handleAllChecksReply(QString body);
    void handleCheckDefDeply(QString body);
    void connectionStatus(int status);
};

#endif // NCHECKS_H
