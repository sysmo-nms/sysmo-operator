#ifndef ROTATINGFILELOGGER_H
#define ROTATINGFILELOGGER_H

#include "stdio.h"
#include "stdlib.h"

#include <QMutex>
#include <QObject>
#include <QString>
#include <QDesktopServices>
#include <QDebug>
#include <QDir>
#include <QCoreApplication>
#include <QThread>
#include <QByteArray>
#include <QIODevice>

#if QT_VERSION >= 0x050000
#include <QMessageLogContext>
#endif

class RotatingFileLogger : public QObject
{
public:
    explicit RotatingFileLogger(QObject* parent = 0);
    ~RotatingFileLogger();
    static RotatingFileLogger* getLogger();

#if QT_VERSION >= 0x050000
    static void log(
            QtMsgType type,
            const QMessageLogContext &context,
            const QString &msg);
#else
    static void log(
            QtMsgType type,
            const char *msg);
#endif

private:
    static RotatingFileLogger* singleton;
    static QMutex mtx;
    QString lock;
    QFile*  logFile;
};

#endif // ROTATINGFILELOGGER_H
