#include "monitorchannel.h"

MonitorChannel::MonitorChannel(QString chan_name, QObject *parent) : QObject(parent)
{
    this->channel = chan_name;
    qDebug() << "should register to channel: " << channel;
    SupercastSignal* sig = new SupercastSignal(this);
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleServerEvent(QJsonObject)));
    Supercast::subscribe(chan_name, sig);
}

MonitorChannel::~MonitorChannel()
{
    emit this->channelDeleted(this->channel);
    qDebug() << "should unregister channel: " << channel;
}

void MonitorChannel::handleServerEvent(QJsonObject event)
{
    if (event.value("type").toString() == "subscribeOk")  return;
    if (event.value("type").toString() == "subscribeErr") return;
    if (event.value("type").toString() == "nchecksSimpleDumpMessage") {
        this->simple_type = true;
        this->simple_file.open();
        this->simple_file.close();
        QString file_name = this->simple_file.fileName();
        QString dump_dir  = event.value("value").toObject().value("httpDumpDir").toString();
        QString dump_file = event.value("value").toObject().value("rrdFile").toString();
        QString http_tmp = "/%1/%2";
        QString http_url = http_tmp.arg(dump_dir).arg(dump_file);
        SupercastSignal* sig = new SupercastSignal(this);
        QObject::connect(
                    sig,  SIGNAL(serverMessage(QString)),
                    this, SLOT(stepHttpReply(QString)));
        Supercast::httpGet(http_url, file_name, sig);
        return;
    }
    if (event.value("type").toString() == "nchecksTableDumpMessage") {
        this->simple_type = false;
        QString dump_dir = event.value("value").toObject().value("httpDumpDir").toString();
        QJsonObject elements_to_files = event.value("value").toObject().value("elementToFile").toObject();
        QStringList elements = elements_to_files.keys();
        QStringListIterator i(elements);
        while (i.hasNext()) {
            QString element = i.next();
            QString dump_file = elements_to_files.value(element).toString();
            QTemporaryFile* file = new QTemporaryFile(this);
            file->open();
            file->close();
            QString file_name = file->fileName();
            this->table_files.insert(element, file);

            QString http_tmp = "/%1/%2";
            QString http_url = http_tmp.arg(dump_dir).arg(dump_file);
            SupercastSignal* sig = new SupercastSignal(this);
            QObject::connect(
                  sig,  SIGNAL(serverMessage(QString)),
                  this, SLOT(stepHttpReply(QString)));
            Supercast::httpGet(http_url, file_name, sig);
        }
        return;
    }
    if (event.value("type").toString() == "nchecksTableUpdateMessage") {
        qDebug() << "table update event" << event;
        return;
    }
    if (event.value("type").toString() == "nchecksSimpleUpdateMessage") {
        qDebug() << "table update event" << event;
        return;
    }
}

void MonitorChannel::stepHttpReply(QString rep) {
    qDebug() << "reply is: " << rep;
}
