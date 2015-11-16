#include "include/monitor/menutarget.h"

MenuTarget::MenuTarget(QWidget* parent) : QMenu(parent)
{
    this->target_name = "undefined";
    /* TODO double clic open actions list QMenu
    this->operation_menu = new QMenu("Operator Actions", this);
    this->operation_menu->setIcon(QIcon(":/icons/utilities-terminal.png"));
    this->addMenu(this->operation_menu);
    */

    //QAction* opconf = new QAction("Configure new Action...", this);
    QAction* opconf = new QAction("Operator Actions...", this);
    opconf->setIcon(QIcon(":/icons/utilities-terminal.png"));
    QObject::connect(
                opconf, SIGNAL(triggered(bool)),
                this, SLOT(handleOperatorActionsConfig()));
    this->addAction(opconf);

    this->addSeparator();

    QAction* add_probe = new QAction("Add a new probe...", this);
    add_probe->setIcon(QIcon(":/icons/list-add.png"));
    this->addAction(add_probe);
    QObject::connect(
                add_probe, SIGNAL(triggered(bool)),
                this,      SLOT(connectNewProbeDialog()));

    this->addSeparator();

    /*
    QAction* dash = new QAction("Dashboard", this);
    dash->setIcon(QIcon(":/icons/utilities-system-monitor.png"));
    this->addAction(dash);
    */

    /*
    QAction* doc = new QAction("Documentation", this);
    doc->setIcon(QIcon(":/icons/folder-saved-search.png"));
    this->addAction(doc);
    */

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
    qDebug() << "show menu for target" << target << at;
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
    MessageBox* box = new MessageBox((QWidget *) this->parent());
    box->setIconType(Sysmo::MESSAGE_WARNING);
    box->setModal(true);
    box->setText(
             "This action will permanently delete this target and his probes.");
    box->setInformativeText("Do you want to continue?");
    box->setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    box->setDefaultButton(QMessageBox::No);
    int ret = box->exec();
    if (ret == QMessageBox::No) return;

    QMap<QString,QVariant> query;
    QMap<QString,QVariant> value;
    value.insert("name", this->target_name);
    query.insert("from", "monitor");
    query.insert("type", "deleteTargetQuery");
    query.insert("value", value);

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig,  SIGNAL(serverMessage(QVariant)),
                this, SLOT(deleteTargetReply(QVariant)));
    Supercast::sendQuery(query, sig);
}

void MenuTarget::deleteTargetReply(QVariant reply)
{
    qDebug() << "delete target reply: " << reply;
}

void MenuTarget::handleOperatorActionsConfig()
{
    MonitorActions::openActionFor(this->target_name);
}