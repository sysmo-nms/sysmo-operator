#include "supercasthttp.h"

SupercastHTTP::SupercastHTTP(QObject* parent) : QObject(parent)
{

}

SupercastHTTP::~SupercastHTTP() {}

void SupercastHTTP::handleClientRequest(QString url)
{
    qDebug() << "should handle request" << url;
    emit this->serverReply("hello");
}
