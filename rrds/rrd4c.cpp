#include "rrd4c.h"

Rrd4c* Rrd4c::singleton = NULL;
Rrd4c* Rrd4c::getInstance() {return Rrd4c::singleton;}

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
    this->rrd4qt_proc = new QProcess(parent);
    this->rrd4qt_proc->setProcessEnvironment(QProcessEnvironment::systemEnvironment());
    QObject::connect(
                this->rrd4qt_proc, SIGNAL(started()),
                this, SLOT(procStarted()));
    QObject::connect(
                this->rrd4qt_proc, SIGNAL(finished(int,QProcess::ExitStatus)),
                this, SLOT(procStopped(int,QProcess::ExitStatus)));
    QObject::connect(
                this->rrd4qt_proc, SIGNAL(readyReadStandardError()),
                this, SLOT(procStderrReadyRead()));
    QObject::connect(
                this->rrd4qt_proc, SIGNAL(readyReadStandardOutput()),
                this, SLOT(procStdoutReadyRead()));
    QString proc_path;
#if defined Q_OS_WIN
    proc_path = bat_path;
#else
    proc_path = sh_path;
#endif
    this->rrd4qt_proc->start(proc_path);
}

void Rrd4c::procStarted()
{
    qDebug() << "proc started";
}

void Rrd4c::procStopped(int exitCode, QProcess::ExitStatus exitStatus)
{
    qDebug() << "proc stoped " << exitCode << " " << exitStatus;
}

void Rrd4c::procStderrReadyRead()
{
    qDebug() << "stderr " << this->rrd4qt_proc->readAllStandardError();
}

void Rrd4c::procStdoutReadyRead()
{
    qDebug() << "stdout " << this->rrd4qt_proc->readAllStandardOutput();

}

void Rrd4c::tryConnect(
        QHostAddress host,
        qint16       port)
{
    Rrd4cSocket* socket_t = new Rrd4cSocket(host,port);

    // server -> message -> client
    QObject::connect(
                socket_t, SIGNAL(serverMessage(QJsonObject)),
                this,     SLOT(routeServerMessage(QJsonObject)),
                Qt::QueuedConnection);

    // client -> message -> server
    QObject::connect(
                this,     SIGNAL(clientMessage(QJsonObject)),
                socket_t, SLOT(handleClientMessage(QJsonObject)),
                Qt::QueuedConnection);

    // socket state
    qRegisterMetaType<QAbstractSocket::SocketError>();
    QObject::connect(
                socket_t->socket,
                    SIGNAL(error(QAbstractSocket::SocketError)),
                this,
                    SLOT(socketError(QAbstractSocket::SocketError)),
                Qt::QueuedConnection);
    QObject::connect(
                socket_t->socket, SIGNAL(connected()),
                this,             SLOT(socketConnected()),
                Qt::QueuedConnection);

    socket_t->moveToThread(&this->socket_thread);
    QObject::connect(
                &this->socket_thread, SIGNAL(finished()),
                socket_t,             SLOT(deleteLater()));
    this->socket_thread.start();
}


Rrd4c::~Rrd4c()
{
    this->socket_thread.quit();
    this->socket_thread.wait();

    delete this->queries;
}


/*
 * SLOTS
 */
void Rrd4c::socketConnected()
{

}


void Rrd4c::socketError(QAbstractSocket::SocketError error)
{
    emit this->connectionStatus(error);
}


void Rrd4c::routeServerMessage(QJsonObject msg)
{
    QString msg_type = msg.value("type").toString("undefined");
    if(msg_type == "reply") {

        int  queryId = msg.take("queryId").toInt(10000);
        bool lastPdu = msg.take("lastPdu").toBool(true);
        if (queryId == 10000) return;

        Rrd4cSignal* sig = this->queries->value(queryId);
        emit sig->serverMessage(msg);

        if (lastPdu) {
            this->queries->remove(queryId);
            sig->deleteLater();
        }

        return;
    }
}

void Rrd4c::sendQuery(QJsonObject query, Rrd4cSignal *reply)
{
    int queryId = 0;
    while (Rrd4c::singleton->queries->contains(queryId)) queryId += 1;

    Rrd4c::singleton->queries->insert(queryId, reply);
    query.insert("queryId", queryId);
    emit Rrd4c::singleton->clientMessage(query);
}
