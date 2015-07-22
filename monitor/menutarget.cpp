#include "menutarget.h"

MenuTarget::MenuTarget(QWidget* parent) : QMenu(parent)
{
    this->target_name = "undefined";
    this->operation_menu = new QMenu("Operator Actions", this);
    this->operation_menu->setIcon(QIcon(":/icons/utilities-terminal.png"));
    this->addMenu(this->operation_menu);

    QAction* opconf = new QAction("Configure new Action...", this);
    this->addAction(opconf);

    this->addSeparator();

    QAction* add_probe = new QAction("Add a new probe...", this);
    add_probe->setIcon(QIcon(":/icons/list-add.png"));
    this->addAction(add_probe);
    QObject::connect(
                add_probe, SIGNAL(triggered(bool)),
                this,      SLOT(connectNewProbeDialog()));

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
    QObject::connect(
                delete_target, SIGNAL(triggered(bool)),
                this,          SLOT(deleteTarget()));
}


void MenuTarget::showMenuFor(QString target, QPoint at)
{
    qDebug() << "show menu for target";
    at.setX(at.x() + 12);
    this->target_name = target;
    this->popup(at);
}

/*
 * Is connected to MonitorWidgets::showNewPobeDialog(QString) by
 * MonitorWidgets: Treeview.target_menu. (avoid dependecy loop).
 */
void MenuTarget::connectNewProbeDialog() {
    emit this->openNewProbeDialog(this->target_name);
}

/*
 * Delete target logic and slots
 */
void MenuTarget::deleteTarget()
{
    MessageBox* box = new MessageBox(this);
    box->setIconType(Sysmo::MESSAGE_WARNING);
    box->setModal(true);
    box->setText("This action will permanently delete this target and his probes.");
    box->setInformativeText("Do you want to continue?");
    box->setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    box->setDefaultButton(QMessageBox::No);
    int ret = box->exec();
    if (ret == QMessageBox::No) return;
    QJsonObject query {
        {"from", "monitor"},
        {"type", "deleteTargetQuery"},
        {"value", QJsonObject {
                {"name", this->target_name}
            }
        }
    };
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(deleteTargetReply(QJsonObject)));
    Supercast::sendQuery(query, sig);
}

void MenuTarget::deleteTargetReply(QJsonObject reply)
{
    qDebug() << "delete target reply: " << reply;
}
