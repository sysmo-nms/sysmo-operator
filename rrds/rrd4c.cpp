#include "rrd4c.h"

Rrd4c* Rrd4c::singleton = NULL;
Rrd4c* Rrd4c::getInstance() {return Rrd4c::singleton;}

Rrd4c::~Rrd4c()
{
    emit this->proc->kill();
    this->proc->waitForFinished();
    delete this->proc;
    delete this->queries;
}

Rrd4c::Rrd4c(QObject* parent) : QObject(parent)
{
    Rrd4c::singleton = this;
    this->queries    = new QHash<int, Rrd4cSignal*>();

    /*
     * Java dir setup.
     * Create gradle installDist directory tree under temporary
     * directory.
     */
    QDir d;
    QString bin_dir =  QDir(this->temporary_dir.path()).absoluteFilePath("bin");
    d.mkdir(bin_dir);
    QString lib_dir =  QDir(this->temporary_dir.path()).absoluteFilePath("lib");
    d.mkdir(lib_dir);

    QString bat_path = QDir(bin_dir).absoluteFilePath("rrd4qt.bat");
    QFile   bat(":/rrd4qt/rrd4qt.bat");
    bat.copy(bat_path);

    QString sh_path = QDir(bin_dir).absoluteFilePath("rrd4qt");
    QFile   sh(":/rrd4qt/rrd4qt.sh");
    sh.copy(sh_path);
    QFile sh_final(sh_path);
    sh_final.setPermissions(sh_final.permissions() | QFile::ExeOwner);

    QString rrd4j_jar_path = QDir(lib_dir).absoluteFilePath("rrd4j-2.3-SNAPSHOT.jar");
    QFile   rrd4j(":/rrd4qt/rrd4j.jar");
    rrd4j.copy(rrd4j_jar_path);

    QString rrd4qt_jar_path = QDir(lib_dir).absoluteFilePath("rrd4qt-1.0-SNAPSHOT.jar");
    QFile   rrd4qt(":/rrd4qt/rrd4qt.jar");
    rrd4qt.copy(rrd4qt_jar_path);

    /*
     * Start the server
     */
    this->proc = new QProcess(parent);
    this->proc->setProcessChannelMode(QProcess::SeparateChannels);
    this->proc->setReadChannel(QProcess::StandardOutput);
    QObject::connect(
                this->proc, SIGNAL(started()),
                this, SLOT(procStarted()));
    QObject::connect(
                this->proc, SIGNAL(finished(int,QProcess::ExitStatus)),
                this, SLOT(procStopped(int,QProcess::ExitStatus)));
    QObject::connect(
                this->proc, SIGNAL(readyRead()),
                this, SLOT(procStdoutReadyRead()));

    QObject::connect(
                this->proc, SIGNAL(readyReadStandardError()),
                this, SLOT(procStderrReadyRead()));

    QString proc_path;
#if defined Q_OS_WIN
    proc_path = bat_path;
#else
    proc_path = sh_path;
#endif
    this->proc->start(proc_path);
}

void Rrd4c::procStdoutReadyRead()
{
    qDebug() << "stdout " << this->proc->readAllStandardOutput();
    /*
     * read header to set block_size. Only read when the header is
     * complete.
     */
    if (this->block_size == 0)
    {
        if (this->proc->bytesAvailable() < HEADER_LEN) return;

        QByteArray header = this->proc->read(HEADER_LEN);
        this->block_size = Rrd4c::arrayToInt32(header);
    }


    /*
     * We have the block_size. Only read when the payload is complete.
     */
    if (this->proc->bytesAvailable() < this->block_size) return;


    /*
     * Read and decode the payload.
     */
    QByteArray    payload  = this->proc->read(this->block_size);
    QJsonDocument json_doc = QJsonDocument::fromJson(payload);
    QJsonObject   json_obj = json_doc.object();


    /*
     * Deliver the message
     * TODO
     */


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

void Rrd4c::callRrd(QString msg)
{
    QByteArray  msg_array = msg.toLocal8Bit();
    qint32      msg_size(msg.size());
    this->proc->write(Rrd4c::int32ToArray(msg_size));
    this->proc->write(msg_array.data(), msg_size);
}

qint32 Rrd4c::arrayToInt32(QByteArray source)
{
    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;
}

QByteArray Rrd4c::int32ToArray(qint32 source)
{
    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;
}

void Rrd4c::procStarted()
{
    qDebug() << "proc started";
    this->callRrd("hello from qt");
}

void Rrd4c::procStopped(int exitCode, QProcess::ExitStatus exitStatus)
{
    qDebug() << "proc stoped " << exitCode << " " << exitStatus;
}

void Rrd4c::procStderrReadyRead()
{
    qDebug() << "stderr " << this->proc->readAllStandardError();
}

