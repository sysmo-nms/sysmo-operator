#include "menuprobe.h"

MenuProbe::MenuProbe(QWidget* parent) : QMenu(parent)
{
    this->probe_name = "undefined";


    /* TODO
    QAction* pause = new QAction("Pause/start probe", this);
    this->addAction(pause);
    QObject::connect(
                pause, SIGNAL(triggered(bool)),
                this,  SLOT(handlePauseProbe()));

    */
    //this->addSeparator();

    QAction* perfs = new QAction("Performances...", this);
    perfs->setIcon(QIcon(":/icons/utilities-system-monitor.png"));
    this->addAction(perfs);

    QObject::connect(
                perfs, SIGNAL(triggered(bool)),
                this, SLOT(handleShowPerf()));

    QAction* force = new QAction("Force check", this);
    force->setIcon(QIcon(":/icons/force.png"));
    this->addAction(force);
    QObject::connect(
                force, SIGNAL(triggered(bool)),
                this,  SLOT(handleForceProbe()));


    this->addSeparator();

    QAction* delete_probe = new QAction("Delete this probe", this);
    delete_probe->setIcon(QIcon(":/icons/process-stop.png"));
    this->addAction(delete_probe);
    QObject::connect(
                delete_probe, SIGNAL(triggered(bool)),
                this,         SLOT(handleDeleteProbe()));
}

void MenuProbe::handleShowPerf()
{
    ProbeWindow::openWindow(this->probe_name);
}

void MenuProbe::showMenuFor(QString probe, QPoint at)
{
    qDebug() << "show menu for probe" << probe << at;
    this->probe_name = probe;
    at.setX(at.x() + 12);
    this->popup(at);
}

void MenuProbe::handleForceProbe()
{
    qDebug() << "force probe" << this->probe_name;
    QJsonObject force_msg {
        {"from", "monitor"},
        {"type", "forceProbeQuery"},
        {"value",
            QJsonObject {
                {"name", this->probe_name}
            }
        }
    } ;
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleForceProbeReply(QJsonObject)));
    Supercast::sendQuery(force_msg, sig);
}

void MenuProbe::handleForceProbeReply(QJsonObject reply)
{
    qDebug() << "force probe reply" << reply;
}

void MenuProbe::handleDeleteProbe()
{
    qDebug() << "delete probe" << this->probe_name;

    MessageBox* box = new MessageBox((QWidget *) this->parent());
    box->setIconType(Sysmo::MESSAGE_WARNING);
    box->setModal(true);
    box->setText("This action will permanently delete this probe.");
    box->setInformativeText("Do you want to continue?");
    box->setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    box->setDefaultButton(QMessageBox::No);
    int ret = box->exec();
    if (ret == QMessageBox::No) return;

    QJsonObject delete_msg = QJsonObject {
        {"from", "monitor"},
        {"type", "deleteProbeQuery"},
        {"value", QJsonObject {
                {"name", this->probe_name}
            }
        }
    };

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(handleDeleteProbeReply(QJsonObject)));
    Supercast::sendQuery(delete_msg, sig);
}

void MenuProbe::handleDeleteProbeReply(QJsonObject reply)
{
    Q_UNUSED(reply);
    qDebug() << "delete probe" << this->probe_name;
}

void MenuProbe::handlePauseProbe()
{
    qDebug() << "pause probe" << this->probe_name;
}
