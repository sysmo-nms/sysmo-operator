/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "rrd4qt.h"
#include <config.h>


#include <network/qjson.h>
#include <logs/clog.h>

#include <QThread>
#include <QAbstractSocket>
#include <QStringList>
#include <QDir>
#include <QFile>
#include <QProcessEnvironment>
#include <QIODevice>
#include <QDataStream>
#include <QApplication>
#include <QPalette>
#include <QColor>

Rrd4Qt* Rrd4Qt::singleton = NULL;

Rrd4Qt* Rrd4Qt::getInstance() {
    return Rrd4Qt::singleton;
}

/*
 * Start the java with good arguments and setup signals slots for read/write
 * communication.
 */
Rrd4Qt::Rrd4Qt(QObject* parent) : QObject(parent) {

    Rrd4Qt::singleton = this;

    /*
     * queries contains a map of "int" to signal, where the "int" represent
     * a specific query made by a foreign object, owning the Rrd4QtSignal.
     */
    this->queries = new QMap<int, Rrd4QtSignal*>();

    /*
     * block_size is used for stdin read function.
     */
    this->block_size = 0;

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

    QString java_bin;
#if defined Q_OS_WIN
    QString bat_path = QDir(bin_dir).absoluteFilePath("rrdio.bat");
    QFile bat(":/rrdio/rrdio.bat");
    bat.copy(bat_path);
    java_bin = bat_path;
#else
    QString sh_path = QDir(bin_dir).absoluteFilePath("rrdio");
    QFile sh(":/rrdio/rrdio.sh");
    sh.copy(sh_path);
    QFile sh_file(sh_path);
    sh_file.setPermissions(sh_file.permissions() | QFile::ExeOwner);
    java_bin = sh_path;
#endif

    QFile rrdio(":/rrdio/rrdio.jar");
    QString rrdio_jar_path =
            QDir(lib_dir).absoluteFilePath(RRDIO_JAR);
    rrdio.copy(rrdio_jar_path);

    QFile rrd4j(":/rrdio/rrd4j.jar");
    QString rrd4j_jar_path =
            QDir(lib_dir).absoluteFilePath(RRDIO_RRD4J_JAR);
    rrd4j.copy(rrd4j_jar_path);

    QFile json(":/rrdio/json.jar");
    QString json_jar_path =
            QDir(lib_dir).absoluteFilePath(RRDIO_JSON_JAR);
    json.copy(json_jar_path);

    /*
     * Start the server
     */
    this->proc = new Rrd4QtProc(this);
    this->proc->setProcessChannelMode(QProcess::SeparateChannels);
    this->proc->setReadChannel(QProcess::StandardOutput);
    QObject::connect(
            this->proc, SIGNAL(started()),
            this, SLOT(procStarted()));
    QObject::connect(
            this->proc, SIGNAL(finished(int, QProcess::ExitStatus)),
            this, SLOT(procStopped(int, QProcess::ExitStatus)));
    QObject::connect(
            this->proc, SIGNAL(readyRead()),
            this, SLOT(procStdoutReadyRead()));

    QObject::connect(
            this->proc, SIGNAL(readyReadStandardError()),
            this, SLOT(procStderrReadyRead()));

    // TODO move to a thread
    this->proc->start(java_bin);

}

Rrd4Qt::~Rrd4Qt() {

    this->proc->kill();
    this->proc->waitForFinished();
    delete this->proc;

    QMap<int, Rrd4QtSignal*>::iterator i;
    for (
            i = this->queries->begin();
            i != this->queries->end();
            ++i) {
        Rrd4QtSignal* sig = i.value();
        delete sig;
    }
    delete this->queries;

}

/*
 * Read packet header (len), then iterate while data is available. Use
 * this->query map to trigger the reply message to the registered object.
 */
void Rrd4Qt::procStdoutReadyRead() {

    /*
     * read header to set block_size. Only read when the header is
     * complete.
     */
    if (this->block_size == 0) {
        if (this->proc->bytesAvailable() < HEADER_LEN) return;

        QByteArray header = this->proc->read(HEADER_LEN);
        this->block_size = Rrd4Qt::arrayToInt32(header);
    }

    /*
     * We have the block_size. Only read when the payload is complete.
     */
    if (this->proc->bytesAvailable() < this->block_size) return;


    /*
     * Read and decode the payload.
     */
    QByteArray payload = this->proc->read(this->block_size);
    QVariant json_var = QJson::decode(QString(payload));
    QMap<QString, QVariant> json_obj = json_var.toMap();

    /*
     * Deliver the message
     */
    int queryId = json_obj.value("queryId").toInt();
    Rrd4QtSignal* sig = this->queries->take(queryId);

    sig->emitServerMessage(QVariant(json_obj));
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
        this->proc->emitReadyRead();

}

/*
 * Call RRD and wait for a result message triggered by sig.
 */
void Rrd4Qt::callRrd(QMap<QString, QVariant> msg, Rrd4QtSignal* sig) {

    int queryId = 0;
    while (Rrd4Qt::singleton->queries->contains(queryId)) queryId += 1;
    Rrd4Qt::singleton->queries->insert(queryId, sig);

    msg.insert("queryId", queryId);

    QByteArray json_array = QJson::encode(msg).toLatin1();
    qint32 json_size = json_array.size();
    Rrd4Qt::singleton->proc->write(Rrd4Qt::int32ToArray(json_size));
    Rrd4Qt::singleton->proc->write(json_array.data(), json_size);

}

/*
 * Simple call to RRD.
 */
void Rrd4Qt::callRrd(QMap<QString, QVariant> msg) {

    QByteArray json_array = QJson::encode(msg).toLatin1();
    qint32 json_size(json_array.size());
    Rrd4Qt::singleton->proc->write(Rrd4Qt::int32ToArray(json_size));
    Rrd4Qt::singleton->proc->write(json_array.data(), json_size);

}

qint32 Rrd4Qt::arrayToInt32(QByteArray source) {

    qint32 temp;
    QDataStream data(&source, QIODevice::ReadWrite);
    data >> temp;
    return temp;

}

QByteArray Rrd4Qt::int32ToArray(qint32 source) {

    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;

}

void Rrd4Qt::procStopped(int exitCode, QProcess::ExitStatus exitStatus) {
    emit this->javaStopped();
    if (exitStatus != QProcess::NormalExit) {
        clogWarning("Proc stoped with exit code %i", exitCode)
    }
}

void Rrd4Qt::procStderrReadyRead() {

    clogWarning("Received string from java stderr: %s",
            this->proc->readAllStandardError().data());
}

/*
 * Called once the java process is started to initialize default colors taken
 * from the current theme.
 */
void Rrd4Qt::procStarted() {

    /*
     * Set default Rrd4Qt colors
     */
    QPalette palette = qApp->palette();
    int gridAlpha = 60;

    QColor color_window = palette.color(QPalette::Window);
    QMap<QString, QVariant> cwindow;
    cwindow.insert("red", color_window.red());
    cwindow.insert("blue", color_window.blue());
    cwindow.insert("green", color_window.green());
    cwindow.insert("alpha", color_window.alpha());

    QColor color_base = palette.color(QPalette::Base);
    QMap<QString, QVariant> cbase;
    cbase.insert("red", color_base.red());
    cbase.insert("blue", color_base.blue());
    cbase.insert("green", color_base.green());
    cbase.insert("alpha", color_base.alpha());

    QColor color_dark = palette.color(QPalette::Dark);
    QMap<QString, QVariant> cdark;
    cdark.insert("red", color_dark.red());
    cdark.insert("blue", color_dark.blue());
    cdark.insert("green", color_dark.green());
    cdark.insert("alpha", color_dark.alpha());

    QMap<QString, QVariant> cgrid;
    cgrid.insert("red", color_dark.red());
    cgrid.insert("blue", color_dark.blue());
    cgrid.insert("green", color_dark.green());
    cgrid.insert("alpha", gridAlpha);

    QColor color_shadow = palette.color(QPalette::Shadow);
    QMap<QString, QVariant> cshadow;
    cshadow.insert("red", color_shadow.red());
    cshadow.insert("blue", color_shadow.blue());
    cshadow.insert("green", color_shadow.green());
    cshadow.insert("alpha", color_shadow.alpha());

    QMap<QString, QVariant> cmgrid;
    cmgrid.insert("red", color_shadow.red());
    cmgrid.insert("blue", color_shadow.blue());
    cmgrid.insert("green", color_shadow.green());
    cmgrid.insert("alpha", gridAlpha);

    QColor color_font = palette.color(QPalette::WindowText);
    QMap<QString, QVariant> cfont;
    cfont.insert("red", color_font.red());
    cfont.insert("blue", color_font.blue());
    cfont.insert("green", color_font.green());
    cfont.insert("alpha", color_font.alpha());

    QMap<QString, QVariant> ctransparent;
    ctransparent.insert("red", 0);
    ctransparent.insert("blue", 0);
    ctransparent.insert("green", 0);
    ctransparent.insert("alpha", 0);

    QMap<QString, QVariant> msg;
    msg.insert("type", "color_config");
    msg.insert("queryId", 0);
    msg.insert("BACK", ctransparent);
    msg.insert("CANVAS", cbase);
    msg.insert("SHADEA", cwindow);
    msg.insert("SHADEB", cwindow);
    msg.insert("GRID", cgrid);
    msg.insert("MGRID", cmgrid);
    msg.insert("FONT", cfont);
    msg.insert("FRAME", cwindow);
    msg.insert("ARROW", cshadow);
    msg.insert("XAXIS", cdark);

    Rrd4Qt::callRrd(msg);

}
