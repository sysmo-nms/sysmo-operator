#include "rrd4c.h"

Rrd4c* Rrd4c::singleton = NULL;
Rrd4c* Rrd4c::getInstance() {return Rrd4c::singleton;}

Rrd4c::~Rrd4c()
{
    this->proc->kill();
    this->proc->waitForFinished();
    delete this->proc;
    delete this->queries;
}

Rrd4c::Rrd4c(QObject* parent) : QObject(parent)
{
    Rrd4c::singleton = this;
    this->queries    = new QHash<int, Rrd4cSignal*>();
    this->block_size = 0;

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

    QString rrd4j_jar_path = QDir(lib_dir).absoluteFilePath("rrd4j-2.3-SNAPSHOT.jar");
    QFile   rrd4j(":/rrd4qt/rrd4j.jar");
    rrd4j.copy(rrd4j_jar_path);

    QString rrd4qt_jar_path = QDir(lib_dir).absoluteFilePath("rrd4qt-1.0-SNAPSHOT.jar");
    QFile   rrd4qt(":/rrd4qt/rrd4qt.jar");
    rrd4qt.copy(rrd4qt_jar_path);

    QString json_jar_path = QDir(lib_dir).absoluteFilePath("javax.json-1.0.4.jar");
    QFile   json(":/rrd4qt/json.jar");
    json.copy(json_jar_path);

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

    this->proc->start(proc_path);
}

void Rrd4c::procStdoutReadyRead()
{
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
     */
    int queryId = json_obj.value("queryId").toInt();
    Rrd4cSignal* sig = this->queries->take(queryId);
    emit sig->serverMessage(json_obj);
    sig->deleteLater();

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

void Rrd4c::callRrd(QJsonObject msg, Rrd4cSignal* sig)
{
    int queryId = 0;
    while (Rrd4c::singleton->queries->contains(queryId)) queryId += 1;
    Rrd4c::singleton->queries->insert(queryId, sig);

    msg.insert("queryId", queryId);

    QByteArray json_array(QJsonDocument(msg).toJson(QJsonDocument::Compact));
    qint32     json_size = json_array.size();
    Rrd4c::singleton->proc->write(Rrd4c::int32ToArray(json_size));
    Rrd4c::singleton->proc->write(json_array.data(), json_size);
}

void Rrd4c::callRrd(QJsonObject msg)
{
    QByteArray json_array(QJsonDocument(msg).toJson(QJsonDocument::Compact));
    qint32     json_size(json_array.size());
    Rrd4c::singleton->proc->write(Rrd4c::int32ToArray(json_size));
    Rrd4c::singleton->proc->write(json_array.data(), json_size);
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

void Rrd4c::procStopped(int exitCode, QProcess::ExitStatus exitStatus)
{
    qDebug() << "proc stoped " << exitCode << " " << exitStatus;
}

void Rrd4c::procStderrReadyRead()
{
    qDebug() << "stderr " << this->proc->readAllStandardError();
}



void Rrd4c::procStarted()
{

    /*
     * Set default applicatio palette
     */
    QPalette palette = qApp->palette();

    QColor color_window = palette.color(QPalette::Window);
    QJsonObject cwindow {
        {"red",   color_window.red()},
        {"blue",  color_window.blue()},
        {"green", color_window.green()},
        {"alpha", color_window.alpha()}
    };

    QColor color_base   = palette.color(QPalette::Base);
    QJsonObject cbase {
        {"red",   color_base.red()},
        {"blue",  color_base.blue()},
        {"green", color_base.green()},
        {"alpha", color_base.alpha()}
    };

    QColor color_dark   = palette.color(QPalette::Dark);
    QJsonObject cdark {
        {"red",   color_dark.red()},
        {"blue",  color_dark.blue()},
        {"green", color_dark.green()},
        {"alpha", color_dark.alpha()}
    };

    QColor color_shadow = palette.color(QPalette::Shadow);
    QJsonObject cshadow {
        {"red",   color_shadow.red()},
        {"blue",  color_shadow.blue()},
        {"green", color_shadow.green()},
        {"alpha", color_shadow.alpha()}
    };

    QColor color_font   = palette.color(QPalette::WindowText);
    QJsonObject cfont {
        {"red",   color_font.red()},
        {"blue",  color_font.blue()},
        {"green", color_font.green()},
        {"alpha", color_font.alpha()}
    };

    QJsonObject ctransparent {
        {"red",   0},
        {"blue",  0},
        {"green", 0},
        {"alpha", 0}
    };

    QJsonObject msg {
        {"type",    "color_config"},
        {"queryId", 0},
        {"BACK",    ctransparent},
        {"CANVAS",  cbase},
        {"SHADEA",  cwindow},
        {"SHADEB",  cwindow},
        {"GRID",    cdark},
        {"MGRID",   cshadow},
        {"FONT",    cfont},
        {"FRAME",   cwindow},
        {"ARROW",   cshadow},
        {"XAXIS",   cdark}
    };

    Rrd4c::callRrd(msg);
}
