#include "monitorchannel.h"

MonitorChannel::MonitorChannel(QString chan_name, QObject *parent)
    : QObject(parent)
{
    this->channel = chan_name;
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleServerEvent(QJsonObject)));
    Supercast::subscribe(chan_name, sig);
}

MonitorChannel::~MonitorChannel()
{
    emit this->channelDeleted(this->channel);
}

void MonitorChannel::handleServerEvent(QJsonObject event)
{
    if (event.value("type").toString() == "subscribeOk")  return;
    if (event.value("type").toString() == "subscribeErr") return;

    /*
     * Simple dump and messages
     */
    if (event.value("type").toString() == "nchecksSimpleDumpMessage") {
        this->simple_file.open();
        this->simple_file.close();
        QString file_name = this->simple_file.fileName();
        QString dump_dir  = event.value("value").toObject()
                                 .value("httpDumpDir").toString();
        QString dump_file = event.value("value").toObject()
                                 .value("rrdFile").toString();
        QString http_tmp = "/%1/%2";
        QString http_url = http_tmp.arg(dump_dir).arg(dump_file);
        SupercastSignal* sig = new SupercastSignal();
        QObject::connect(
                    sig,  SIGNAL(serverMessage(QString)),
                    this, SLOT(handleHttpReplySimple(QString)));
        Supercast::httpGet(http_url, file_name, sig);
        return;
    }

    if (event.value("type").toString() == "nchecksSimpleUpdateMessage") {
        if (!this->synchronized) {
            this->pending_updates.enqueue(event);
            return;
        }
        QString file_name = this->simple_file.fileName();
        QJsonObject     val = event.value("value").toObject();
        QJsonObject updates = val.value("rrdupdates").toObject();
        int       timestamp = val.value("timestamp").toInt();
        QJsonObject update_query {
            {"type",      "update"},
            {"updates",   updates},
            {"file",      file_name},
            {"timestamp", timestamp},
            {"opaque",    "undefined"}
        };

        Rrd4cSignal* sig = new Rrd4cSignal();
        QObject::connect(
                    sig, SIGNAL(serverMessage(QJsonObject)),
                    this, SLOT(handleRrdEventSimple(QJsonObject)));
        Rrd4c::callRrd(update_query, sig);
        return;
    }

    /*
     * Table dump and messages
     */
    if (event.value("type").toString() == "nchecksTableDumpMessage") {
        qDebug() << "event table dump: " << event;
        QString dump_dir = event.value("value").toObject()
                                .value("httpDumpDir").toString();
        QJsonObject elements_to_files = event.value("value").toObject()
                                             .value("elementToFile").toObject();
        QStringList elements = elements_to_files.keys();
        QStringListIterator i(elements);
        while (i.hasNext()) {
            QString element = i.next();
            QString dump_file = elements_to_files.value(element).toString();
            QTemporaryFile* file = new QTemporaryFile(this);
            file->open();
            file->close();
            QString file_name = file->fileName();

            qDebug() << "table fname: " << file_name;
            QString http_tmp = "/%1/%2";
            QString http_url = http_tmp.arg(dump_dir).arg(dump_file);
            SupercastSignal* sig = new SupercastSignal();
            QObject::connect(
                  sig,  SIGNAL(serverMessage(QString)),
                  this, SLOT(handleHttpReplyTable(QString)));
            Supercast::httpGet(http_url, file_name, sig, element);
            this->table_files.insert(element, file_name);
            this->table_files_update_status.insert(element, false);

        }
        return;
    }
    if (event.value("type").toString() == "nchecksTableUpdateMessage") {
        if (!this->synchronized) {
            this->pending_updates.enqueue(event);
            return;
        }

        QJsonObject val       = event.value("value").toObject();
        QJsonObject updates   = val.value("rrdupdates").toObject();
        int         timestamp = val.value("timestamp").toInt();
        QStringList updates_indexes = updates.keys();
        QStringListIterator i(updates_indexes);
        this->table_file_rrd_pending.clear();
        while (i.hasNext()) {
            QString id       = i.next();
            QString tRrdFile = this->table_files.value(id);
            QJsonObject up = updates.value(id).toObject();
            QJsonObject update_query {
                {"type",      "update"},
                {"updates",   up},
                {"file",      tRrdFile},
                {"timestamp", timestamp},
                {"opaque",    id}
            };
            this->table_file_rrd_pending.insert(id, true);

            Rrd4cSignal* sig = new Rrd4cSignal();
            QObject::connect(
                        sig,  SIGNAL(serverMessage(QJsonObject)),
                        this, SLOT(handleRrdEventTable(QJsonObject)));
            Rrd4c::callRrd(update_query, sig);
        }
        qDebug() << "table update event" << updates;
        return;
    }
}

void MonitorChannel::handleRrdEventTable(QJsonObject event)
{
    QString id = event.value("opaque").toString();
    this->table_file_rrd_pending.insert(id, false);

    QHash<QString, bool>::iterator i;
    bool pending_rrds = false;
    for (
         i  = this->table_file_rrd_pending.begin();
         i != this->table_file_rrd_pending.end();
         ++i)
    {
        if (i.value()) {
            pending_rrds = true;
            break;
        }
    }
    if (!pending_rrds) {
        qDebug() << "updating rrds ended!!!!!!!!!!!!!!";
        qDebug() << "should emit update table graph";
    }
}

void MonitorChannel::handleRrdEventSimple(QJsonObject event)
{
    qDebug() << "rrd simple event reply" << event;
    qDebug() << "should emit update simple graph";
}

void MonitorChannel::handleHttpReplySimple(QString rep) {
    qDebug() << "reply is: " << rep;
    this->synchronized = true;
    while (!this->pending_updates.isEmpty())
        this->handleServerEvent(this->pending_updates.dequeue());

    qDebug() << "should emit update simple graph";

}

void MonitorChannel::handleHttpReplyTable(QString element) {
    this->table_files_update_status.insert(element, true);

    bool all_files_ready = true;
    QHash<QString, bool>::iterator i;
    for (
         i  = this->table_files_update_status.begin();
         i != this->table_files_update_status.end();
         ++i)
    {
        if (!i.value()) {
            all_files_ready = false;
            break;
        }
    }

    if (all_files_ready) {
        qDebug() << "all files ready!!!!!!!!!!!!";
        this->synchronized = true;
        while (!this->pending_updates.isEmpty())
                this->handleServerEvent(this->pending_updates.dequeue());
        qDebug() << "should emit update table graph";
    }
}
