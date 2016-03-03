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
#ifndef RRD4QTGRAPH_H
#define RRD4QTGRAPH_H

#include "rrd4qt.h"
#include "rrd4qtsignal.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QTemporaryFile>
#include <QPixmap>
#include <QDebug>
#include <QVariant>
#include <QMap>

class Rrd4QtGraph : public QLabel
{
    Q_OBJECT
public:
    explicit Rrd4QtGraph(
            QString     rrd_db_file,
            QMap<QString,QVariant> rrd_graph_config,
            int         initial_height,
            QWidget*    parent = 0);

private:
    QMap<QString,QVariant> graph_config;
    QString       graph_id;
    QString       pixmap_file;
    QPixmap       pixmap_obj;

public slots:
    void handleRrdReply(QVariant reply);
    void setTimeSpan(int time_span);
    void setGraphHeight(int height);
    void setGraphWidth(int width);
};

#endif // RRD4QTGRAPH_H
