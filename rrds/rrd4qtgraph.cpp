#include "rrd4qtgraph.h"

Rrd4QtGraph::Rrd4QtGraph(
        QString     rrd_db_file,
        QJsonObject rrd_graph_config,
        QWidget*    parent) : QLabel(parent)
{
    QTemporaryFile* f = new QTemporaryFile(this);
    f->open();
    f->close();
    this->graph_config = rrd_graph_config;
    this->graph_config.insert("rrdFile", QJsonValue(rrd_db_file));
    this->graph_config.insert("pngFile", QJsonValue(f->fileName()));
    this->graph_config.insert("height", QJsonValue(300));
    this->graph_config.insert("width", QJsonValue(400));
    this->graph_config.insert("type", QJsonValue("graph"));
    this->graph_config.insert("opaque", QJsonValue(""));
    this->graph_config.insert("spanBegin", QJsonValue(-300));
    this->graph_config.insert("spanEnd", QJsonValue(0));

    qDebug() << "should graph: " << this->graph_config.keys() << f->fileName();

    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleRrdReply(QJsonObject)));
    Rrd4Qt::callRrd(this->graph_config, sig);
}

void Rrd4QtGraph::handleRrdReply(QJsonObject reply)
{
    qDebug() << "get reply: " << reply;
}
