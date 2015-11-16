#include "include/rrds/rrd4qtgraph.h"

Rrd4QtGraph::Rrd4QtGraph(
        QString     rrd_db_file,
        QMap<QString,QVariant> rrd_graph_config,
        int         initial_height,
        QWidget*    parent) : QLabel(parent)
{
    /*
     * Open and close temporary file to generate fileName()
     */
    QTemporaryFile* f = new QTemporaryFile(this);
    f->open();
    f->close();
    this->pixmap_file = f->fileName();


    /*
     * User the allready created json object but complete it
     * with values needed to graph.
     */
    this->graph_config = rrd_graph_config;

    this->graph_config.insert("rrdFile",   rrd_db_file);
    this->graph_config.insert("pngFile",   this->pixmap_file);
    this->graph_config.insert("height",    initial_height);
    this->graph_config.insert("width",     400);
    this->graph_config.insert("type",      "graph");
    this->graph_config.insert("opaque",    "");
    this->graph_config.insert("spanBegin", -300000);
    this->graph_config.insert("spanEnd",   0);


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
                sig,   SIGNAL(serverMessage(QVariant)),
                this,  SLOT(handleRrdReply(QVariant)));

    Rrd4Qt::callRrd(this->graph_config, sig);

}

void Rrd4QtGraph::handleRrdReply(QVariant reply_var)
{
    QMap<QString,QVariant> reply = reply_var.toMap();
    if (reply.value("reply") == "success")
    {
        this->pixmap_obj.load(this->pixmap_file);
        this->setPixmap(this->pixmap_obj);
        return;
    }

    qWarning() << "callRrd graph returned:" << reply;
}

void Rrd4QtGraph::setTimeSpan(int time_span)
{
    qDebug() << "set time span";
    this->graph_config.insert("spanBegin", 0 - time_span);
    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
                sig,   SIGNAL(serverMessage(QVariant)),
                this,  SLOT(handleRrdReply(QVariant)));

    Rrd4Qt::callRrd(this->graph_config, sig);
}

void Rrd4QtGraph::setGraphHeight(int height)
{
    this->graph_config.insert("height", height);
    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
                sig,   SIGNAL(serverMessage(QVariant)),
                this,  SLOT(handleRrdReply(QVariant)));

    Rrd4Qt::callRrd(this->graph_config, sig);
}

void Rrd4QtGraph::setGraphWidth(int width)
{
    if (width < 250) {
        qDebug() << "is min than 250";
        width = 250;
    }

    qDebug() << "change width to: " << width;
    this->graph_config.insert("width", width);
    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
                sig,   SIGNAL(serverMessage(QVariant)),
                this,  SLOT(handleRrdReply(QVariant)));

    Rrd4Qt::callRrd(this->graph_config, sig);
}
