#include "nchecks.h"

NChecks::NChecks(QObject *parent) : QObject(parent)
{
    QObject::connect(
                Supercast::getInstance(), SIGNAL(connectionStatus(int)),
                this, SLOT(connectionStatus(int)));
}

void NChecks::connectionStatus(int status)
{

    if (status != Supercast::ConnectionSuccess) return;

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QString)),
                this, SLOT(handleAllChecksReply(QString)));
    Supercast::httpGet("/nchecks/AllChecks.xml", sig);
}

void NChecks::handleAllChecksReply(QString body)
{
    qDebug() << "nchecks network reply" << body;
}
