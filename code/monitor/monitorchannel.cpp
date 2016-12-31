/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
                sig,  SIGNAL(serverMessage(QVariant)),
                this, SLOT(handleServerEvent(QVariant)));

    Supercast::subscribe(this->channel, sig);

}


MonitorChannel::~MonitorChannel()
{

    emit this->channelDeleted(this->channel);

}


void MonitorChannel::handleServerEvent(QVariant event_variant)
{

    QMap<QString,QVariant> event = event_variant.toMap();
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
        QString dump_dir  = event.value("value").toMap()
                                 .value("httpDumpDir").toString();
        QString dump_file = event.value("value").toMap()
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
        QMap<QString,QVariant> content =   event.value("value").toMap();
        QMap<QString,QVariant> updates = content.value("rrdupdates").toMap();
        int timestamp = content.value("timestamp").toInt();


        /*
         * Create rrd query message
         */
        QMap<QString,QVariant> update_query;
        update_query.insert("type", "update");
        update_query.insert("updates", updates);
        update_query.insert("file", this->simple_file.fileName());
        update_query.insert("timestamp", timestamp);
        update_query.insert("opaque", "undefined");

        /*
         * Connect signals for callback
         */
        Rrd4QtSignal* sig = new Rrd4QtSignal();
        QObject::connect(
                    sig, SIGNAL(serverMessage(QVariant)),
                    this, SLOT(handleRrdEventSimple(QVariant)));

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
        QMap<QString,QVariant> content = event.value("value").toMap();
        QString       dump_dir = content.value("httpDumpDir").toString();
        QMap<QString,QVariant> id_to_file = content.value("elementToFile").toMap();


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
        QMap<QString,QVariant> content = event.value("value").toMap();
        QMap<QString,QVariant> updates = content.value("rrdupdates").toMap();
        int timestamp = content.value("timestamp").toInt();


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
            QMap<QString,QVariant> up = updates.value(id).toMap();

            /*
             * Build query
             */
            QMap<QString,QVariant> update_query;
            update_query.insert("type", "update");
            update_query.insert("updates", up);
            update_query.insert("file", rrd_file);
            update_query.insert("timestamp", timestamp);
            update_query.insert("opaque", id);

            /*
             * Connect signals for callback
             */
            Rrd4QtSignal* sig = new Rrd4QtSignal();
            QObject::connect(
                        sig,  SIGNAL(serverMessage(QVariant)),
                        this, SLOT(handleRrdEventTable(QVariant)));

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


void MonitorChannel::handleRrdEventTable(QVariant event_variant)
{

    QMap<QString,QVariant> event = event_variant.toMap();
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
    QMap<QString, bool>::iterator i;
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
        QMap<QString,QVariant> update_msg;
        update_msg.insert("event", "update");

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


void MonitorChannel::handleRrdEventSimple(QVariant event_variant)
{

    Q_UNUSED(event_variant);

    /*
     * Emit message of type update
     */
    QMap<QString,QVariant> update_msg;
    update_msg.insert("event", "update");
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
    QMap<QString, bool>::iterator i;
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


QMap<QString,QVariant> MonitorChannel::getDumpInfo()
{

    return this->buildDump();

}


QMap<QString,QVariant> MonitorChannel::buildDump()
{

    /*
     * If chan is "simple" the buildDump is simple
     */
    if (this->chan_type == "simple") {
        QMap<QString,QVariant> dumpEvent;
        dumpEvent.insert("event", "dump");
        dumpEvent.insert("type", "simple");
        dumpEvent.insert("rrdFile", this->simple_file.fileName());
        return dumpEvent;
    }
    if (this->chan_type == "table") {
        QMap<QString,QVariant> table_dump;

        /*
         * If chan is "table", we need to iterate over table_files
         */
        QMap<QString,QString>::iterator i;
        for (i = this->table_files.begin();
                 i != this->table_files.end(); ++i)
        {
            table_dump.insert(i.key(), i.value());
        }

        QMap<QString,QVariant> dumpEvent;
        dumpEvent.insert("event", "dump");
        dumpEvent.insert("type", "table");
        dumpEvent.insert("rrdFiles", table_dump);

        return dumpEvent;
    }

    /*
     * Should never occur.
     */
    qCritical() <<
              "buildDump() called with wrong chan_type: " << this->chan_type;
    return QMap<QString,QVariant>();
   
}
