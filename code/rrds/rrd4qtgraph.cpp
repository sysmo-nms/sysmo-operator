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
#include "rrd4qtgraph.h"

#include "rrd4qt.h"
#include "rrd4qtsignal.h"

#include <logs/clog.h>

#include <QObject>
#include <QTemporaryFile>

Rrd4QtGraph::Rrd4QtGraph(
        QString rrd_db_file,
        QMap<QString, QVariant> rrd_graph_config,
        int initial_height,
        QWidget* parent) : QLabel(parent) {

    /*
     * Open and close temporary file to generate fileName()
     */
    QTemporaryFile* f = new QTemporaryFile(this);
    f->open();
    f->close();
    this->pixmap_file = f->fileName();


    /*
     * Use the allready created json object but complete it
     * with values needed to graph.
     */
    this->graph_config = rrd_graph_config;

    this->graph_config.insert("rrdFile", rrd_db_file);
    this->graph_config.insert("pngFile", this->pixmap_file);
    this->graph_config.insert("height", initial_height);
    this->graph_config.insert("width", 400);
    this->graph_config.insert("type", "graph");
    this->graph_config.insert("opaque", "");
    this->graph_config.insert("spanBegin", -300000);
    this->graph_config.insert("spanEnd", 0);


    /*
     * Temporary set the text label with graph title.
     * Will be overhiden by the later callRrd().
     */
    this->setText(this->graph_config.value("label").toString());



    /*
     * Call rrd to graph initial pixmap;
     */
    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
            sig, SIGNAL(serverMessage(QVariant)),
            this, SLOT(handleRrdReply(QVariant)));

    Rrd4Qt::callRrd(this->graph_config, sig);

}

void Rrd4QtGraph::handleRrdReply(QVariant reply_var) {

    QMap<QString, QVariant> reply = reply_var.toMap();
    if (reply.value("reply") == "success") {
        this->pixmap_obj.load(this->pixmap_file);
        this->setPixmap(this->pixmap_obj);
        return;
    }

}

void Rrd4QtGraph::updateGraphConf(int width, int height, int span) {

    clogDebug("Change width to: %i, height to: %i, and span to: %i ", width, height, span);

    if (width < 250)
        width = 250;
    this->graph_config.insert("width", width);
    this->graph_config.insert("height", height);
    this->graph_config.insert("spanBegin", 0 - span);

    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
            sig, SIGNAL(serverMessage(QVariant)),
            this, SLOT(handleRrdReply(QVariant)));

    Rrd4Qt::callRrd(this->graph_config, sig);

}
