#include "monitor.h"

Monitor* Monitor::singleton = NULL;

Monitor* Monitor::getInstance() {return Monitor::singleton;}

Monitor::Monitor(QObject *parent) : QObject(parent)
{
    Monitor::singleton = this;
    this->targets  = new QHash<QString, QJsonObject>();
    this->probes   = new QHash<QString, QJsonObject>();
    this->channels = new QHash<QString, MonitorChannel*>();

}


Monitor::~Monitor()
{
    delete this->targets;
    delete this->probes;
    delete this->channels;
}

QWidget* Monitor::getCenterWidget()
{
    return dynamic_cast<QWidget*>(Monitor::singleton->parent());
}

void Monitor::handleServerMessage(QJsonObject message)
{
    QString         type = message.value("type").toString("undefined");
    QJsonObject mcontent = message.value("value").toObject();

    if (type == "infoTarget") {
        QString	tname(mcontent.value("name").toString(""));

        this->targets->insert(tname,mcontent);
        emit this->infoTarget(mcontent);


    } else if (type == "infoProbe") {
        QString	pname(mcontent.value("name").toString(""));

        this->probes->insert(pname, mcontent);
        emit this->infoProbe(mcontent);


    } else if (type == "deleteTarget") {
        QString	tname(mcontent.value("name").toString(""));

        this->targets->remove(tname);
        emit this->deleteTarget(mcontent);


    } else if (type == "deleteProbe") {
        QString	pname(mcontent.value("name").toString(""));

        this->targets->remove(pname);
        emit this->deleteProbe(mcontent);


    } else if (type == "probeReturn") {
        emit this->probeReturn(mcontent);

    } else if (type == "syncEnd") {
        emit this->initialSyncEnd();

    } else if (type == "nchecksSimpleDumpMessage") {
    } else if (type == "nchecksSimpleUpdateMessage") {
    } else if (type == "nchecksTableDumpMessage") {
    } else if (type == "nchecksTableUpdateMessage") {
    } else if (type == "subscribeOk") {
    } else if (type == "unSubscribeOk") {
    } else {
        QJsonDocument doc(message);
        qWarning() << "received message!!" << type << doc.toJson();
   }
}


QJsonObject Monitor::getTarget(QString targetId)
{
    return Monitor::singleton->targets->value(targetId);
}

QJsonObject Monitor::getProbe(QString probeId)
{
    return Monitor::singleton->probes->value(probeId);
}

void Monitor::channelDeleted(QString chan_name)
{
    this->channels->remove(chan_name);
}


void Monitor::unsubscribeToChannel(
        QString             channel,
        MonitorProxyWidget* subscriber)
{
    Monitor* mon = Monitor::getInstance();

    /*
     * If channel exist, else should not append.
     */
    if (mon->channels->contains(channel))
    {
        MonitorChannel* chan = mon->channels->value(channel);
        chan->disconnect(subscriber);
        chan->decreaseSubscriberCount();
    } else {
        qWarning() << "Call unsubscribeToChannel for unknonw channel" << channel;
    }
}


void Monitor::subscribeToChannel(
        QString             channel,
        MonitorProxyWidget* subscriber)
{
    Monitor* mon = Monitor::getInstance();

    /*
     * If channel exist
     */
    if (mon->channels->contains(channel)) {
        /*
         * get the channel and increase his subscriber count.
         */
        MonitorChannel* chan = mon->channels->value(channel);
        chan->increaseSubscriberCount();

        /*
         * If the channel has some dumpInfos (has received dumps from the
         * server), get this dumpInfo and forward it to the channel.
         */
        if (chan->hasDumpInfo()) {
            QJsonObject dump = chan->getDumpInfo();
            subscriber->handleEvent(dump);
        }

        /*
         * Then connect the channel to the subscriber
         */
        QObject::connect(
                    chan,       SIGNAL(channelEvent(QJsonObject)),
                    subscriber, SLOT(handleEvent(QJsonObject)));
    } else {
        /*
         * Channel do not exist, create it. And increase his subscriber
         * count.
         */
        MonitorChannel* chan = new MonitorChannel(channel, mon);
        chan->increaseSubscriberCount();

        /*
         * I want (Monitor) to be informed of the deletion of the channel,
         * with his channel name (destroyed() signal unusable here.
         */
        QObject::connect(
                    chan, SIGNAL(channelDeleted(QString)),
                    mon,  SLOT(channelDeleted(QString)));

        /*
         * Insert channel in my Channels hash
         */
        mon->channels->insert(channel, chan);

        /*
         * Connect the subscriber to the channel then.
         *
         * INFO: the channel will not have dumpInfo until at least the
         * control return to the main loop. No need to check hasDumpInfo()
         */
        QObject::connect(
                    chan,       SIGNAL(channelEvent(QJsonObject)),
                    subscriber, SLOT(handleEvent(QJsonObject)));
    }
}




MonitorProxyWidget::MonitorProxyWidget(
        QString channel,
        QWidget *parent) : QWidget(parent)
{
    this->my_channel = channel;

    /*
     * Require delayed connect, to hava initialized subclass of
     * MonitorProxyWidget successfuly reply to "handleEvent" virtual
     * slot. This is a single shot.
     */
    QObject::connect(
                this, SIGNAL(connectMe()),
                this, SLOT(connectToChannel()),
                Qt::QueuedConnection);
    emit this->connectMe();
}

void MonitorProxyWidget::connectToChannel()
{
    Monitor::subscribeToChannel(this->my_channel, this);
}

MonitorProxyWidget::~MonitorProxyWidget()
{
    Monitor::unsubscribeToChannel(this->my_channel, this);
}
