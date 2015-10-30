#include "monitorchannel.h"

MonitorChannel::MonitorChannel(QString chan_name, QObject *parent)
    : QObject(parent)
{
    this->sync_dir = "sync";
    this->channel = chan_name;
    this->chan_type = "none";
    this->subscriber_count = 0;
    this->synchronized = false;
    this->locked = false;

    /*
     * Connect and subscribe to this->channel supercast channel
     */
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleServerEvent(QJsonObject)));

    Supercast::subscribe(this->channel, sig);
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
     * SIMPLE EVENTS
     */
    if (event.value("type").toString() == "nchecksSimpleDumpMessage") {
        /*
         * set this object of type simple
         */
        this->chan_type = "simple";


        /*
         * get http dump dir and file
         */
        QString dump_dir  = event.value("value").toObject()
                                 .value("httpDumpDir").toString();
        QString dump_file = event.value("value").toObject()
                                 .value("rrdFile").toString();

        /*
         * build url
         */
        QString http_tmp = "/%1/%2/%3";
        QString http_url = http_tmp.arg(this->sync_dir).arg(dump_dir).arg(dump_file);


        /*
         * Create and connect signal for callback
         */
        SupercastSignal* sig = new SupercastSignal();
        QObject::connect(
                    sig,  SIGNAL(serverMessage(QString)),
                    this, SLOT(handleHttpReplySimple(QString)));


        /*
         * Open close temporary file to generate fileName()
         */
        this->simple_file.open();
        this->simple_file.close();


        /*
         * get the file and put it in tmpfile.fileName()
         */
        Supercast::httpGet(http_url, this->simple_file.fileName(), sig);

        /*
         * end
         */
        return;
    }

    if (event.value("type").toString() == "nchecksSimpleUpdateMessage") {
        /*
         * Do not accept events while not synchronized or another
         * event is not yet completely processed.
         * Equeue it for later processing.
         */
        if (!this->synchronized || this->locked) {
            this->pending_updates.enqueue(event);
            return;
        } else this->locked = true;


        /*
         * Extract update informations
         */
        QJsonObject content =   event.value("value").toObject();
        QJsonObject updates = content.value("rrdupdates").toObject();
        int       timestamp = content.value("timestamp").toInt();


        /*
         * Create rrd query message
         */
        QJsonObject update_query;
        update_query.insert("type", QJsonValue("update"));
        update_query.insert("updates", updates);
        update_query.insert("file", QJsonValue(this->simple_file.fileName()));
        update_query.insert("timestamp", QJsonValue(timestamp));
        update_query.insert("opaque", QJsonValue("undefined"));

        /*
         * Connect signals for callback
         */
        Rrd4QtSignal* sig = new Rrd4QtSignal();
        QObject::connect(
                    sig, SIGNAL(serverMessage(QJsonObject)),
                    this, SLOT(handleRrdEventSimple(QJsonObject)));

        /*
         * Call rrd to update rrd
         */
        Rrd4Qt::callRrd(update_query, sig);


        /*
         * end
         */
        return;
    }


    /*
     * TABLE EVENTS
     */
    if (event.value("type").toString() == "nchecksTableDumpMessage") {
        /*
         * set this object of type simple
         */
        this->chan_type = "table";


        /*
         * Extract dump informations
         */
        QJsonObject    content =   event.value("value").toObject();
        QString       dump_dir = content.value("httpDumpDir").toString();
        QJsonObject id_to_file = content.value("elementToFile").toObject();


        /*
         * Iterate over json elementToFile key/value
         */
        QStringListIterator i(id_to_file.keys());
        while (i.hasNext()) {
            /*
             * Extract element id and dump_file
             */
            QString elem_id   = i.next();
            QString dump_file = id_to_file.value(elem_id).toString();


            /*
             * Create and initialize temporary file to hav a
             * valid fileName()
             */
            QTemporaryFile* file = new QTemporaryFile(this);
            file->open();
            file->close();
            this->table_files.insert(elem_id, file->fileName());


            /*
             * Set this element_id file status to false
             */
            this->table_files_update_status.insert(elem_id, false);


            /*
             * Generate url
             */
            QString http_tmp = "/%1/%2/%3";
            QString http_url = http_tmp.arg(this->sync_dir).arg(dump_dir).arg(dump_file);
            qDebug() << "http dump dir is: " << http_url;


            /*
             * Create and connect signal for callback
             */
            SupercastSignal* sig = new SupercastSignal();
            QObject::connect(
                  sig,  SIGNAL(serverMessage(QString)),
                  this, SLOT(handleHttpReplyTable(QString)));

            /*
             * get the file
             */
            Supercast::httpGet(http_url, file->fileName(), sig, elem_id);
        }
        /*
         * end
         */
        return;
    }

    if (event.value("type").toString() == "nchecksTableUpdateMessage") {
        /*
         * Do not accept events while not synchronized or another
         * event is not yet completely processed.
         * Equeue it for later processing.
         */
        if (!this->synchronized || this->locked) {
            this->pending_updates.enqueue(event);
            return;
        } else this->locked = true;


        /*
         * Extract update informations
         */
        QJsonObject   content =   event.value("value").toObject();
        QJsonObject   updates = content.value("rrdupdates").toObject();
        int         timestamp = content.value("timestamp").toInt();


        /*
         * Clear previous file update pending hash
         */
        this->table_file_rrd_pending.clear();


        /*
         * Iterate over all the table updates and send rrd update
         * query
         */
        QStringListIterator i(updates.keys());
        while (i.hasNext()) {
            QString id       = i.next();

            /*
             * Add an entry to pending hash
             */
            this->table_file_rrd_pending.insert(id, true);

            /*
             * Get the fileName corresponding to id
             */
            QString rrd_file = this->table_files.value(id);

            /*
             * Extract updates as is (jsonObject)
             */
            QJsonObject up = updates.value(id).toObject();

            /*
             * Build query
             */
            QJsonObject update_query;
            update_query.insert("type", QJsonValue("update"));
            update_query.insert("updates", up);
            update_query.insert("file", QJsonValue(rrd_file));
            update_query.insert("timestamp", QJsonValue(timestamp));
            update_query.insert("opaque", QJsonValue(id));

            /*
             * Connect signals for callback
             */
            Rrd4QtSignal* sig = new Rrd4QtSignal();
            QObject::connect(
                        sig,  SIGNAL(serverMessage(QJsonObject)),
                        this, SLOT(handleRrdEventTable(QJsonObject)));

            /*
             * call rrd update
             */
            Rrd4Qt::callRrd(update_query, sig);
        }
        /*
         * end
         */
        return;
    }

    qWarning() << "handleServerMessage unknown message type" << event;
}

void MonitorChannel::handleRrdEventTable(QJsonObject event)
{
    /*
     * Extract opaque set in handlerServerEvent() from event
     */
    QString id = event.value("opaque").toString();


    /*
     * Update table pending state
     */
    this->table_file_rrd_pending.insert(id, false);


    /*
     * Iterate pending rrds. If one value is true,
     * break. The update is not yet finished.
     */
    bool pending_rrds = false;
    QHash<QString, bool>::iterator i;
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

    /*
     * If there are no more rrds to update
     */
    if (!pending_rrds) {
        /*
         * Emit an update message to the connected widgets
         */
        QJsonObject update_msg;
        update_msg.insert("event", QJsonValue("update"));

        emit this->channelEvent(update_msg);


        /*
         * Unlock the channel for other events processing
         */
        this->locked = false;


        /*
         * But first handle allready queued messages.
         * WARNING: this lead to a recursive call, wich can in case of buggy
         * server lead to a buffer overflow.
         * TODO: use signal -> slot QtQueuedConnection.
         */
        if (!this->pending_updates.isEmpty())
            this->handleServerEvent(this->pending_updates.dequeue());
    }
}



void MonitorChannel::handleRrdEventSimple(QJsonObject event)
{
    Q_UNUSED(event);

    /*
     * Emit message of type update
     */
    QJsonObject update_msg;
    update_msg.insert("event", QJsonValue("update"));
    emit this->channelEvent(update_msg);


    /*
     * Unlock the channel for future events
     */
    this->locked = false;


    /*
     * But first handle allready queued messages.
     * WARNING: this lead to a recursive call, wich can in case of buggy
     * server lead to a buffer overflow.
     * TODO: use signal -> slot QtQueuedConnection.
     */
    if (!this->pending_updates.isEmpty())
        this->handleServerEvent(this->pending_updates.dequeue());
}



void MonitorChannel::handleHttpReplySimple(QString rep)
{
    Q_UNUSED(rep);

    /*
     * Simple http reply, the channel should be synchronized
     */
    this->synchronized = true;


    /*
     * Emit a dump event for connected widgets
     */
    emit this->channelEvent(this->buildDump());


    /*
     * But first handle allready queued messages.
     * WARNING: this lead to a recursive call, wich can in case of buggy
     * server lead to a buffer overflow.
     * TODO: use signal -> slot QtQueuedConnection.
     */
    if (!this->pending_updates.isEmpty())
        this->handleServerEvent(this->pending_updates.dequeue());
}

void MonitorChannel::handleHttpReplyTable(QString element) {

    /*
     * Update the status of the file in the hash table
     */
    this->table_files_update_status.insert(element, true);


    /*
     * Iterate file_update_status, set files read to false and break
     * if one update_status is false.
     */
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


    /*
     * If all files have arrived, this is the end of the http multiple calls.
     */
    if (all_files_ready) {
        /*
         * Now the channel should be synchronized
         */
        this->synchronized = true;


        /*
         * Emit dump event to connected widgets
         */
        emit this->channelEvent(this->buildDump());


        /*
         * But first handle allready queued messages.
         * WARNING: this lead to a recursive call, wich can in case of buggy
         * server lead to a buffer overflow.
         * TODO: use signal -> slot QtQueuedConnection.
         */
        if (!this->pending_updates.isEmpty())
            this->handleServerEvent(this->pending_updates.dequeue());
    }
}

void MonitorChannel::increaseSubscriberCount(){this->subscriber_count += 1;}
void MonitorChannel::decreaseSubscriberCount()
{
    this->subscriber_count -= 1;

    /*
     * If subscriber count reach 0, the channel have no utilities.
     * Disconnect from Supercast and close then.
     */
    if (this->subscriber_count == 0) {
        Supercast::unsubscribe(this->channel);
        this->deleteLater();
    }
}

bool        MonitorChannel::hasDumpInfo() {return this->synchronized;}
QJsonObject MonitorChannel::getDumpInfo()
{
    return this->buildDump();
}

QJsonObject MonitorChannel::buildDump()
{
    /*
     * If chan is "simple" the buildDump is simple
     */
    if (this->chan_type == "simple") {
        QJsonObject dumpEvent;
        dumpEvent.insert("event", QJsonValue("dump"));
        dumpEvent.insert("type", QJsonValue("simple"));
        dumpEvent.insert("rrdFile", QJsonValue(this->simple_file.fileName()));
        return dumpEvent;
    }
    if (this->chan_type == "table") {
        QJsonObject table_dump;

        /*
         * If chan is "table", we need to iterate over table_files
         */
        QHash<QString,QString>::iterator i;
        for (i = this->table_files.begin();
                 i != this->table_files.end(); ++i)
        {
            table_dump.insert(i.key(), QJsonValue(i.value()));
        }

        QJsonObject dumpEvent;
        dumpEvent.insert("event", QJsonValue("dump"));
        dumpEvent.insert("type", QJsonValue("table"));
        dumpEvent.insert("rrdFiles", table_dump);

        return dumpEvent;
    }

    /*
     * Should never occur.
     */
    qCritical() <<
              "buildDump() called with wrong chan_type: " << this->chan_type;
    return QJsonObject();
}
