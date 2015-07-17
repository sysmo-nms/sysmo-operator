#ifndef RRD4C_H
#define RRD4C_H

#include "rrds/rrd4csignal.h"

#include <QObject>
#include <QJsonObject>
#include <QThread>
#include <QAbstractSocket>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QStringList>
#include <QHash>
#include <QTemporaryDir>
#include <QDir>
#include <QFile>
#include <QProcess>
#include <QProcessEnvironment>
#include <QByteArray>
#include <QIODevice>
#include <QDataStream>
#include <QJsonDocument>
#include <QApplication>
#include <QPalette>
#include <QColor>

#include <QDebug>


class Rrd4c : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4c(QObject* parent = 0);
    ~Rrd4c();
    static Rrd4c* getInstance();
    static void callRrd(QJsonObject msg, Rrd4cSignal* sig);
    static void callRrd(QJsonObject msg);

public slots:
    void procStarted();
    void procStopped(int exitCode, QProcess::ExitStatus exitStatus);
    void procStdoutReadyRead();
    void procStderrReadyRead();

private:
    static Rrd4c*             singleton;
    static const qint32       HEADER_LEN = 4;
    qint32                    block_size;
    QTemporaryDir             temporary_dir;
    QProcess*                 proc = NULL;
    QHash<int, Rrd4cSignal*>* queries = NULL;
    static qint32     arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32 source);

};

#endif // RRD4C_H
