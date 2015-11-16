#ifndef RRD4QT_H
#define RRD4QT_H

#include "include/rrds/rrd4qtsignal.h"
#include "include/rrds/rrd4qtproc.h"
#include "include/qjson.h"
#include "include/temporarydir.h"

#include <QObject>
#include <QThread>
#include <QAbstractSocket>
#include <QStringList>
#include <QMap>
#include <QDir>
#include <QFile>
#include <QProcess>
#include <QProcessEnvironment>
#include <QByteArray>
#include <QIODevice>
#include <QDataStream>
#include <QApplication>
#include <QPalette>
#include <QColor>
#include <QVariant>

#include <QDebug>


class Rrd4Qt : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4Qt(QObject* parent = 0);
    ~Rrd4Qt();
    static Rrd4Qt* getInstance();
    static void callRrd(QMap<QString,QVariant> msg, Rrd4QtSignal* sig);
    static void callRrd(QMap<QString,QVariant> msg);

public slots:
    void procStarted();
    void procStopped(int exitCode, QProcess::ExitStatus exitStatus);
    void procStdoutReadyRead();
    void procStderrReadyRead();

signals:
    void javaStopped();

private:
    static Rrd4Qt* singleton;
    static const int HEADER_LEN = 4;

    qint32        block_size;
    TemporaryDir temporary_dir;
    //QTemporaryDir temporary_dir; // Qt4 incompatible

    Rrd4QtProc* proc;
    QMap<int, Rrd4QtSignal*>* queries;

    static qint32     arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32     source);

};

#endif // RRD4QT_H
