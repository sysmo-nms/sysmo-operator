#include "nchecks.h"

NChecks::NChecks(QObject *parent) : QObject(parent)
{
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleNetworkReply(QJsonObject)));
    Supercast::httpGet("http://www.sysmo.io", sig);
}

void NChecks::handleNetworkReply(QJsonObject obj)
{
    qDebug() << "nchecks network reply" << obj;
}
