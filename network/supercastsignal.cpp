#include "supercastsignal.h"

SupercastSignal::SupercastSignal(QObject* parent) : QObject(parent) {}

void SupercastSignal::emitServerMessage(int integer) {
    emit this->serverMessage(integer);
}

void SupercastSignal::emitServerMessage(QString string) {
    emit this->serverMessage(string);
}

void SupercastSignal::emitServerMessage(QVariant json) {
    emit this->serverMessage(json);
}
