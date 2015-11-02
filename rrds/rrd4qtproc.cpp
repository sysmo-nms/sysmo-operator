#include "rrd4qtproc.h"

Rrd4QtProc::Rrd4QtProc(QObject* parent) : QProcess(parent)
{

}

void Rrd4QtProc::emitReadyRead() {
    emit this->readyRead();
}
