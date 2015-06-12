#include "menutarget.h"

MenuTarget::MenuTarget(QWidget* parent) : QMenu(parent)
{
    this->operation_menu = new QMenu("Operator Actions", this);
    this->operation_menu->setIcon(QIcon(":/icons/utilities-terminal.png"));
    this->addMenu(this->operation_menu);

    QAction* opconf = new QAction("Configure new Action...", this);
    this->addAction(opconf);

    this->addSeparator();

    QAction* add_probe = new QAction("Add a new probe...", this);
    add_probe->setIcon(QIcon(":/icons/list-add.png"));
    this->addAction(add_probe);

    // catch triggered
    QObject::connect(
                add_probe, SIGNAL(triggered(bool)),
                this,      SLOT(connectNewProbeDialog()));
    // and forward with a string argument
    /*
    QObject::connect(
                this,   SIGNAL(openNewProbeDialog(QString)),
                Monitor::getInstance(), SLOT(newProbe(QString)));
                */

    this->addSeparator();

    QAction* dash = new QAction("Dashboard", this);
    dash->setIcon(QIcon(":/icons/utilities-system-monitor.png"));
    this->addAction(dash);

    QAction* doc = new QAction("Documentation", this);
    doc->setIcon(QIcon(":/icons/folder-saved-search.png"));
    this->addAction(doc);

    this->addSeparator();

    QAction* delete_target = new QAction("Delete this target", this);
    delete_target->setIcon(QIcon(":/icons/process-stop.png"));
    this->addAction(delete_target);
}


void MenuTarget::showMenuFor(QString target, QPoint at)
{
    qDebug() << "show menu for target";
    at.setX(at.x() + 12);
    this->target_name = target;
    this->popup(at);
}

void MenuTarget::connectNewProbeDialog() {
    emit this->openNewProbeDialog(this->target_name);

}
