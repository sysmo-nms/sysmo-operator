#include "menuprobe.h"

MenuProbe::MenuProbe(QWidget* parent) : QMenu(parent)
{
    this->probe_name = "undefined";

    QAction* force = new QAction("Force check", this);
    force->setIcon(QIcon(":/icons/force.png"));
    this->addAction(force);
    QObject::connect(
                force, SIGNAL(triggered(bool)),
                this,  SLOT(handleForceProbe()));

    QAction* pause = new QAction("Pause/start probe", this);
    this->addAction(pause);
    QObject::connect(
                pause, SIGNAL(triggered(bool)),
                this,  SLOT(handlePauseProbe()));

    this->addSeparator();

    QAction* perfs = new QAction("Performances", this);
    perfs->setIcon(QIcon(":/icons/utilities-system-monitor.png"));
    this->addAction(perfs);

    this->addSeparator();

    QAction* delete_probe = new QAction("Delete this probe", this);
    delete_probe->setIcon(QIcon(":/icons/process-stop.png"));
    this->addAction(delete_probe);
    QObject::connect(
                delete_probe, SIGNAL(triggered(bool)),
                this,         SLOT(handleDeleteProbe()));
}


void MenuProbe::showMenuFor(QString probe, QPoint at)
{
    qDebug() << "show menu for probe";
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
    };
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
}

void MenuProbe::handlePauseProbe()
{
    qDebug() << "pause probe" << this->probe_name;
}
