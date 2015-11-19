#include "include/rotatingfilelogger.h"

RotatingFileLogger* RotatingFileLogger::singleton = new RotatingFileLogger();
QMutex RotatingFileLogger::mtx;

RotatingFileLogger::~RotatingFileLogger()
{
    QFile::remove(this->lock);
    this->logFile->close();
}

RotatingFileLogger::RotatingFileLogger(QObject* parent) : QObject(parent)
{
    // see http://doc.qt.io/qt-5/qtglobal.html
#if !defined QT_DEBUG
    qputenv("QT_LOGGING_RULES", "qt.network.ssl.warning=false");
#endif

    QString logDir;
#if QT_VERSION >= 0x050000
    logDir = QStandardPaths::writableLocation(QStandardPaths::DataLocation);
#else
    logDir = QDesktopServices::storageLocation(QDesktopServices::DataLocation);
#endif
    QString sysmoLogDir =
            QDir::cleanPath(logDir + QDir::separator() + "sysmo_logs");

    QDir dirUtil(sysmoLogDir);
    if (!dirUtil.exists(sysmoLogDir)) {
        dirUtil.mkdir(sysmoLogDir);
    }

    int logFileId = 0;
    int appPid = QCoreApplication::applicationPid();

    QString logFilePath;
    while (true) {
        QString lockFile  = "sysmo-" + QString::number(logFileId) + ".log.lck";
        QString lockFilePath = dirUtil.filePath(lockFile);
        QFile l(lockFilePath);
        if (l.exists()) {
            // lock exist try next
            logFileId += 1;
            continue;
        }

        if (!l.open(QIODevice::Append)) {
            // on windows the file can be allready locked
            logFileId += 1;
            continue;
        }

        l.write(QString::number(appPid).toLatin1());
        l.close();

        // for now lock file contain our pid
        l.open(QIODevice::ReadOnly);
        QTextStream in(&l);
        QString content = in.readAll();
        if (!content.startsWith(QString::number(appPid))) {
            // Another pid has locked the file before us or will not lock it at
            // all because content may be truncated in wich case this lock is
            // unusable for all concurent lockers.
            logFileId += 1;
            continue;
        }

        // We own the lock
        this->lock = lockFilePath;
        QString logFile  = "sysmo-" + QString::number(logFileId) + ".log";
        logFilePath = dirUtil.filePath(logFile);
        break;
    }
    this->logFile = new QFile(logFilePath);
    this->logFile->open(QIODevice::Append);
}

RotatingFileLogger* RotatingFileLogger::getLogger()
{
    if (RotatingFileLogger::singleton == NULL) {
        RotatingFileLogger::singleton = new RotatingFileLogger();
    }
    return RotatingFileLogger::singleton;
}


#if QT_VERSION >= 0x050000
void RotatingFileLogger::log(
        QtMsgType type,
        const QMessageLogContext &context,
        const QString &msg)
{
    Q_UNUSED(context);
    RotatingFileLogger::mtx.lock();
    QByteArray logMsg = msg.toLocal8Bit();
    switch (type) {
    case QtDebugMsg:
        QString head = "\nDebug: ";
        RotatingFileLogger::singleton->logFile->write(head.toLocal8Bit());
        RotatingFileLogger::singleton->logFile->write(logMsg);
        break;
    case QtWarningMsg:
        QString head = "\nWarning: ";
        RotatingFileLogger::singleton->logFile->write(head.toLocal8Bit());
        RotatingFileLogger::singleton->logFile->write(logMsg);
        break;
    case QtCriticalMsg:
        QString head = "\nCritical: ";
        RotatingFileLogger::singleton->logFile->write(head.toLocal8Bit());
        RotatingFileLogger::singleton->logFile->write(logMsg);
        break;
    case QtFatalMsg:
        QString head = "\nFatal: ";
        RotatingFileLogger::singleton->logFile->write(head.toLocal8Bit());
        RotatingFileLogger::singleton->logFile->write(logMsg);
        abort();
    default:
        break;
    }
    RotatingFileLogger::mtx.unlock();
}

#else
void RotatingFileLogger::log(
        QtMsgType type,
        const char *msg)
{
    QByteArray logMsg(msg);
    RotatingFileLogger::mtx.lock();
    switch (type) {
    case QtDebugMsg:
    case QtWarningMsg:
        char head[10] = "\nWarning: ";
        RotatingFileLogger::singleton->logFile->write(&head);
        RotatingFileLogger::singleton->logFile->write(logMsg);
        break;
    case QtCriticalMsg:
        char head[11] = "\nCritical: ";
        RotatingFileLogger::singleton->logFile->write(&head);
        RotatingFileLogger::singleton->logFile->write(logMsg);
        break;
    case QtFatalMsg:
        char head[8] = "\nFatal: ";
        RotatingFileLogger::singleton->logFile->write(&head);
        RotatingFileLogger::singleton->logFile->write(logMsg);
        break
    default:
        break;
    }
    RotatingFileLogger::mtx.unlock();
}
#endif
