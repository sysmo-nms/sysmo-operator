#include "menuprobe.h"

MenuProbe::MenuProbe(QWidget* parent) : QMenu(parent)
{

    QAction* force = new QAction("Force check", this);
    force->setIcon(QIcon(":/icons/force.png"));
    this->addAction(force);

    QAction* pause = new QAction("Pause/start probe", this);
    this->addAction(pause);

    this->addSeparator();

    QAction* perfs = new QAction("Performances...", this);
    perfs->setIcon(QIcon(":/icons/utilities-system-monitor.png"));
    this->addAction(perfs);

    this->addSeparator();

    QAction* delete_probe = new QAction("Delete this probe...", this);
    delete_probe->setIcon(QIcon(":/icons/process-stop.png"));
    this->addAction(delete_probe);
}


void MenuProbe::showMenuFor(QString target, QPoint at)
{
    qDebug() << "show menu for probe";
    at.setX(at.x() + 12);
    this->popup(at);

}
