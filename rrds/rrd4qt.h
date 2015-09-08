#ifndef RRD4QT_H
#define RRD4QT_H

#include "rrds/rrd4qtsignal.h"

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


class Rrd4Qt : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4Qt(QObject* parent = 0);
    ~Rrd4Qt();
    static Rrd4Qt* getInstance();
    static void callRrd(QJsonObject msg, Rrd4QtSignal* sig);
    static void callRrd(QJsonObject msg);

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
    QTemporaryDir temporary_dir;

    QProcess*                  proc;
    QHash<int, Rrd4QtSignal*>* queries;

    static qint32     arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32     source);

};

#endif // RRD4QT_H
