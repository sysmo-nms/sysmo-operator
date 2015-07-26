#include "rrd4qtproc.h"

Rrd4QtProc::~Rrd4QtProc()
{
    this->proc->kill();
    this->proc->waitForFinished();
    delete this->proc;

}

Rrd4QtProc::Rrd4QtProc(QObject* parent) : QObject(parent)
{
    this->block_size  = 0;

    /*
     * Java dir setup.
     * Create gradle installDist directory tree under temporary
     * directory.
     */
    QString bin_dir = QDir(this->temporary_dir.path()).absoluteFilePath("bin");
    QString lib_dir = QDir(this->temporary_dir.path()).absoluteFilePath("lib");

    QDir d;
    d.mkdir(bin_dir);
    d.mkdir(lib_dir);

    QString proc_path;
#if defined Q_OS_WIN
    QString bat_path = QDir(bin_dir).absoluteFilePath("rrd4qt.bat");
    QFile   bat(":/rrd4qt/rrd4qt.bat");
    bat.copy(bat_path);
    proc_path = bat_path;
#else
    QString sh_path = QDir(bin_dir).absoluteFilePath("rrd4qt");
    QFile   sh(":/rrd4qt/rrd4qt.sh");
    sh.copy(sh_path);
    QFile sh_file(sh_path);
    sh_file.setPermissions(sh_file.permissions() | QFile::ExeOwner);
    proc_path = sh_path;
#endif

    QFile   rrd4j(":/rrd4qt/rrd4j.jar");
    QString rrd4j_jar_path =
            QDir(lib_dir).absoluteFilePath("rrd4j-3.0-SYSMO-SNAPSHOT.jar");
    rrd4j.copy(rrd4j_jar_path);

    QFile   rrd4qt(":/rrd4qt/rrd4qt.jar");
    QString rrd4qt_jar_path =
            QDir(lib_dir).absoluteFilePath("rrd4qt-1.0-SNAPSHOT.jar");
    rrd4qt.copy(rrd4qt_jar_path);

    QFile   json(":/rrd4qt/json.jar");
    QString json_jar_path =
            QDir(lib_dir).absoluteFilePath("javax.json-1.0.4.jar");
    json.copy(json_jar_path);

    /*
     * Start the server
     */
    this->proc = new QProcess(parent);
    this->proc->setProcessChannelMode(QProcess::SeparateChannels);
    this->proc->setReadChannel(QProcess::StandardOutput);
    QObject::connect(
                this->proc, SIGNAL(started()),
                this,       SLOT(procStarted()));
    QObject::connect(
                this->proc, SIGNAL(finished(int,QProcess::ExitStatus)),
                this,       SLOT(procStopped(int,QProcess::ExitStatus)));
    QObject::connect(
                this->proc, SIGNAL(readyRead()),
                this,       SLOT(procStdoutReadyRead()));

    QObject::connect(
                this->proc, SIGNAL(readyReadStandardError()),
                this,       SLOT(procStderrReadyRead()));

    this->proc->start(proc_path);
}

void Rrd4QtProc::procStdoutReadyRead()
{
    /*
     * read header to set block_size. Only read when the header is
     * complete.
     */
    if (this->block_size == 0)
    {
        if (this->proc->bytesAvailable() < HEADER_LEN) return;

        QByteArray header = this->proc->read(HEADER_LEN);
        this->block_size = Rrd4QtProc::arrayToInt32(header);
    }

    /*
     * We have the block_size. Only read when the payload is complete.
     */
    if (this->proc->bytesAvailable() < this->block_size) return;


    /*
     * Read and decode the payload.
     */
    QByteArray     payload = this->proc->read(this->block_size);
    QJsonDocument json_doc = QJsonDocument::fromJson(payload);
    QJsonObject   json_obj = json_doc.object();

    /*
     * Deliver the message
     */
    emit this->replyMsg(json_obj);

    /*
     * Reinitialize block size to 0
     */
    this->block_size = 0;

    /*
     * Emit aditional readyRead() wich will call this function again
     * without recursion (QueuedConnection).
     */
    if (this->proc->bytesAvailable() != 0)
        emit this->proc->readyRead();
}

qint32 Rrd4QtProc::arrayToInt32(QByteArray source)
{
    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;
}

QByteArray Rrd4QtProc::int32ToArray(qint32 source)
{
    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;
}

void Rrd4QtProc::procStopped(int exitCode, QProcess::ExitStatus exitStatus)
{
    emit this->javaStopped();
    qDebug() << "proc stoped " << exitCode << " " << exitStatus;
}

void Rrd4QtProc::procStderrReadyRead()
{
    qDebug() << "stderr " << this->proc->readAllStandardError();
}

void Rrd4QtProc::procStarted()
{

}
