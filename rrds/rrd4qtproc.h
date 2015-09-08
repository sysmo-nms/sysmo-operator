#ifndef RRD4QTPROC_H
#define RRD4QTPROC_H

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

class Rrd4QtProc : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4QtProc(QObject* parent = 0);
    ~Rrd4QtProc();

public slots:
    void procStarted();
    void procStopped(int exitCode, QProcess::ExitStatus exitStatus);
    void procStdoutReadyRead();
    void procStderrReadyRead();

signals:
    void javaStopped();
    void replyMsg(QJsonObject msg);

private:
    static const qint32 HEADER_LEN = 4;

    qint32        block_size;
    QTemporaryDir temporary_dir;
    QProcess*     proc;

    static qint32     arrayToInt32(QByteArray source);
    static QByteArray int32ToArray(qint32     source);

};
#endif // RRD4QTPROC_H
