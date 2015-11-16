#include "include/rrds/rrd4qtsignal.h"

Rrd4QtSignal::Rrd4QtSignal(QObject* parent) : QObject(parent) {}

void Rrd4QtSignal::emitServerMessage(int integer) {
    emit this->serverMessage(integer);
}

void Rrd4QtSignal::emitServerMessage(QString string) {
    emit this->serverMessage(string);
}

void Rrd4QtSignal::emitServerMessage(QVariant json) {
    emit this->serverMessage(json);
}
