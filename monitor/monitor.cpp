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


void Monitor::handleServerMessage(QJsonObject message)
{
    QString     type = message.value("type").toString("undefined");
    QJsonValue  mvalues(message.value("value"));
    QJsonObject mcontent = mvalues.toObject();

    if (type == "infoTarget") {
        QString	    tname(mcontent.value("name").toString(""));

        this->targets->insert(tname,mcontent);
        emit this->infoTarget(mcontent);


    } else if (type == "infoProbe") {
        QString	    pname(mcontent.value("name").toString(""));

        this->probes->insert(pname, mcontent);
        emit this->infoProbe(mcontent);


    } else if (type == "deleteTarget") {
        QString	    tname(mcontent.value("name").toString(""));

        this->targets->remove(tname);
        emit this->deleteTarget(mcontent);


    } else if (type == "deleteProbe") {
        QString	    pname(mcontent.value("name").toString(""));

        this->targets->remove(pname);
        emit this->deleteProbe(mcontent);


    } else if (type == "probeReturn") {
        emit this->probeReturn(mcontent);


    } else if (type == "nchecksSimpleDumpMessage") {
    } else if (type == "nchecksSimpleUpdateMessage") {
    } else if (type == "nchecksTableDumpMessage") {
    } else if (type == "nchecksTableUpdateMessage") {
    } else if (type == "subscribeOk") {
    } else if (type == "unSubscribeOk") {
    } else {
        QJsonDocument doc(message);
        qDebug() << "received message!!" << type;
        qDebug() << doc.toJson();
   }
}

void Monitor::channelDeleted(QString chan_name)
{
    qDebug() << "remove chan Monitor";
    this->channels->remove(chan_name);
}

void Monitor::unsubscribeToChannel(QString channel)
{
    Monitor* mon = Monitor::getInstance();
    if (mon->channels->contains(channel)) {
        MonitorChannel* chan = mon->channels->value(channel);
        chan->decreaseSubscriberCount();
    }
}

void Monitor::subscribeToChannel(
        QString channel,
        MonitorProxyWidget* subscriber)
{
    // TEST BEGIN
    QJsonObject ex {
        {"from", "jojojojoj"}
    };
    subscriber->handleEvent(ex);
    // TEST END

    Monitor* mon = Monitor::getInstance();
    if (mon->channels->contains(channel)) {
        MonitorChannel* chan = mon->channels->value(channel);
        chan->increaseSubscriberCount();
    } else {
        MonitorChannel* chan = new MonitorChannel(channel, mon);
        QObject::connect(
                    chan, SIGNAL(channelDeleted(QString)),
                    mon,  SLOT(channelDeleted(QString)));
        chan->increaseSubscriberCount();
        mon->channels->insert(channel, chan);
    }
}




MonitorProxyWidget::MonitorProxyWidget(
        QString channel,
        QWidget *parent) : QWidget(parent)
{
    this->my_channel = channel;
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
    qDebug() << "close chann proxy";
    Monitor::unsubscribeToChannel(this->my_channel);
}

