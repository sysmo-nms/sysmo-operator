#include "monitorchannel.h"

MonitorChannel::MonitorChannel(QString probe_name)
{
    qDebug() << "Constructor called: " << probe_name;

}

MonitorChannel::~MonitorChannel()
{
    qDebug() << "Destructor called";
}
