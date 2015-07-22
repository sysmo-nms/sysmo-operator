#include "rrd4qtgraph.h"

Rrd4QtGraph::Rrd4QtGraph(
        QString     rrd_db_file,
        QJsonObject rrd_graph_config,
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
     * User the allready created QJsonObject but complete it
     * with values needed to graph.
     */
    this->graph_config = rrd_graph_config;

    this->graph_config.insert("rrdFile",   QJsonValue(rrd_db_file));
    this->graph_config.insert("pngFile",   QJsonValue(this->pixmap_file));
    this->graph_config.insert("height",    QJsonValue(200));
    this->graph_config.insert("width",     QJsonValue(400));
    this->graph_config.insert("type",      QJsonValue("graph"));
    this->graph_config.insert("opaque",    QJsonValue(""));
    this->graph_config.insert("spanBegin", QJsonValue(-300000));
    this->graph_config.insert("spanEnd",   QJsonValue(0));


    /*
     * Temporary set the text label with graph title.
     * Will be overhiden by the later callRrd().
     */
    this->setText(this->graph_config.value("label").toString());


    /*
     * Connect signal
     * TODO keep the same signal for emiting and receiving
     * WARNING if signal is emited when i am destroyed.
     */
    Rrd4QtSignal* sig = new Rrd4QtSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleRrdReply(QJsonObject)));


    /*
     * Call rrd to graph initial pixmap;
     */
    Rrd4Qt::callRrd(this->graph_config, sig);

}

void Rrd4QtGraph::handleRrdReply(QJsonObject reply)
{
    if (reply.value("reply") == "success")
    {
        this->pixmap_obj.load(this->pixmap_file);
        this->setPixmap(this->pixmap_obj);
        return;
    }

    qWarning() << "callRrd graph returned:" << reply;
}
