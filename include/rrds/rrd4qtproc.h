#ifndef RRD4QTPROC_H
#define RRD4QTPROC_H

#include <QObject>
#include <QProcess>

class Rrd4QtProc : public QProcess
{

public:
    Rrd4QtProc(QObject* parent = 0);
    void emitReadyRead();
};

#endif // RRD4QTPROC_H
