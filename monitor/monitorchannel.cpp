#include "monitorchannel.h"

MonitorChannel::MonitorChannel(QString chan_name, QObject *parent)
    : QObject(parent)
{
    qDebug() << "new channel?????";
    this->channel = chan_name;
    SupercastSignal* sig = new SupercastSignal(this);
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleServerEvent(QJsonObject)));
    /*
    QObject::connect(
                qApp, SIGNAL(aboutToQuit()),
                this, SLOT(deleteLater()));
                */
    Supercast::subscribe(chan_name, sig);
}

MonitorChannel::~MonitorChannel()
{
    qDebug() << "deleted??? ";
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
        this->chan_type = "simple";
        this->simple_file.open();
        this->simple_file.close();
        QString file_name = this->simple_file.fileName();
        QString dump_dir  = event.value("value").toObject()
                                 .value("httpDumpDir").toString();
        QString dump_file = event.value("value").toObject()
                                 .value("rrdFile").toString();
        QString http_tmp = "/%1/%2";
        QString http_url = http_tmp.arg(dump_dir).arg(dump_file);
        SupercastSignal* sig = new SupercastSignal(this);
        QObject::connect(
                    sig,  SIGNAL(serverMessage(QString)),
                    this, SLOT(handleHttpReplySimple(QString)));
        Supercast::httpGet(http_url, file_name, sig);
        return;
    }

    if (event.value("type").toString() == "nchecksSimpleUpdateMessage") {
        if (!this->synchronized || this->locked) {
            this->pending_updates.enqueue(event);
            return;
        }
        this->locked = true;
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
        this->chan_type = "table";
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
            SupercastSignal* sig = new SupercastSignal(this);
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
        if (!this->synchronized || this->locked) {
            this->pending_updates.enqueue(event);
            return;
        }
        this->locked = true;

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
        emit this->channelEvent(QJsonObject {{"type", "update"}});
        this->locked = false;
        if (!this->pending_updates.isEmpty())
            this->handleServerEvent(this->pending_updates.dequeue());
    }
}

void MonitorChannel::handleRrdEventSimple(QJsonObject event)
{
    Q_UNUSED(event);
    emit this->channelEvent(QJsonObject {{"type", "update"}});
    this->locked = false;
    if (!this->pending_updates.isEmpty())
        this->handleServerEvent(this->pending_updates.dequeue());
}

void MonitorChannel::handleHttpReplySimple(QString rep) {
    Q_UNUSED(rep);
    this->synchronized = true;
    this->locked = false;
    emit this->channelEvent(this->buildDump());
    if (!this->pending_updates.isEmpty())
        this->handleServerEvent(this->pending_updates.dequeue());
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
        this->synchronized = true;
        this->locked = false;
        emit this->channelEvent(this->buildDump());
        if (!this->pending_updates.isEmpty())
            this->handleServerEvent(this->pending_updates.dequeue());
    }
}

void MonitorChannel::increaseSubscriberCount()
{
    this->subscriber_count += 1;
}

void MonitorChannel::decreaseSubscriberCount()
{
    this->subscriber_count -= 1;
    if (this->subscriber_count == 0) {
        qDebug() << "decrease and close";
        Supercast::unsubscribe(this->channel);
        this->deleteLater();
    }
}

bool MonitorChannel::hasDumpInfo() {return this->synchronized;}
QJsonObject MonitorChannel::getDumpInfo()
{
    return this->buildDump();
}

QJsonObject MonitorChannel::buildDump()
{
    if (this->chan_type == "simple") {
        return QJsonObject {
            {"type", "simple"},
            {"file", this->simple_file.fileName()}
        };
    } else if (this->chan_type == "table") {
        QJsonObject id_to_files;
        QHash<QString,QString>::iterator i;
        for (
             i  = this->table_files.begin();
             i != this->table_files.end();
             ++i)
        {
            id_to_files.insert(i.key(), QJsonValue(i.value()));
        }

        return QJsonObject {
            {"type",        "table"},
            {"id_to_files", id_to_files}
        };
    } else {
        return QJsonObject();
    }
}
