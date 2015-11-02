#include "monitoractionsdialog.h"

MonitorActionsDialog::MonitorActionsDialog(QWidget* parent, QString target)
    : QDialog(parent)
{
    this->target = target;
    NGrid* grid = new NGrid();
    this->setLayout(grid);

    this->setMinimumHeight(200);
    this->setMinimumWidth(300);

    //QSettings s;
    //QHash<QString, QVariant> acts = s.value("actions/monitoractions").toHash();

    QPushButton* addAction = new QPushButton(this);
    addAction->setText("New...");
    addAction->setIcon(QIcon(":/icons/list-add.png"));
    QObject::connect(
                addAction, SIGNAL(clicked(bool)),
                this, SLOT(handleAddAction()));

    this->delAction = new QPushButton(this);
    delAction->setText("Delete...");
    QObject::connect(
                delAction, SIGNAL(clicked(bool)),
                this, SLOT(handleDelAction()));

    this->editAction = new QPushButton(this);
    editAction->setText("Edit...");
    QObject::connect(
                editAction, SIGNAL(clicked(bool)),
                this, SLOT(handleEditAction()));

    this->list_view  = new QListWidget(this);
    this->list_view->setSelectionMode(QAbstractItemView::SingleSelection);
    QObject::connect(
                this->list_view, SIGNAL(itemSelectionChanged()),
                this,            SLOT(handleSelectionChange()));
    QObject::connect(
                this->list_view, SIGNAL(itemDoubleClicked(QListWidgetItem*)),
                this, SLOT(handleDoubleClicked(QListWidgetItem*)));

    /*
     * button box
     */
    QDialogButtonBox *buttonBox = new QDialogButtonBox(this);
    buttonBox->addButton(QDialogButtonBox::Close);
    QPushButton *close = buttonBox->button(QDialogButtonBox::Close);
    QObject::connect(
                close, SIGNAL(clicked(bool)),
                this,  SLOT(close()));
    grid->addWidget(addAction, 0,0);
    grid->addWidget(this->editAction, 3,0);
    grid->addWidget(this->delAction, 4,0);
    grid->addWidget(list_view, 0,1,5,1);
    grid->addWidget(buttonBox, 5,0,1,2);

    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);
    grid->setRowStretch(2,0);
    grid->setRowStretch(3,0);
    grid->setRowStretch(4,0);

    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    this->updateView();
}

void MonitorActionsDialog::updateView()
{
    this->list_view->clear();
    this->handleSelectionChange();
    QSettings s;
    QHash<QString, QVariant> acts = s.value("actions/monitoractions").toHash();
    QVariant var = acts.value(this->target);


    if (!var.isValid()) return;

    QHash<QString, QVariant> actionConf = var.toHash();

    QHashIterator<QString, QVariant> i(actionConf);
    while (i.hasNext()) {
        i.next();
        this->list_view->addItem(i.key());
    }
}

void MonitorActionsDialog::handleDoubleClicked(QListWidgetItem *item)
{
    QString name = item->data(Qt::DisplayRole).toString();

    QSettings s;
    QHash<QString, QVariant> acts = s.value("actions/monitoractions").toHash();
    QHash<QString, QVariant> tconf = acts.value(this->target).toHash();
    QHash<QString, QVariant> aconf = tconf.value(name).toHash();

    QString cmd = aconf.value("cmd").toString();
    QString args = aconf.value("args").toString();

    QStringList args_list = args.split(" ");
    qDebug() << "should execute " << cmd << " with args " << args;
    ActionProcess *proc = new ActionProcess();
    proc->startProcess(cmd, args_list);
    this->close();
}

void MonitorActionsDialog::handleDelAction()
{
    QList<QListWidgetItem*> selection = this->list_view->selectedItems();
    QListWidgetItem *item = selection.at(0);
    QString name = item->data(Qt::DisplayRole).toString();

    MessageBox msgbox(this);
    msgbox.setIconType(Sysmo::MESSAGE_WARNING);
    msgbox.setText("Do you want to delete the action: " + name + "?");
    msgbox.setStandardButtons(QMessageBox::Yes | QMessageBox::No);

    if (msgbox.exec() == QMessageBox::No) return;

    QSettings s;
    QHash<QString, QVariant> acts = s.value("actions/monitoractions").toHash();
    QHash<QString, QVariant> targetConf = acts.value(this->target).toHash();
    targetConf.remove(name);
    acts.insert(this->target, QVariant(targetConf));
    s.setValue("actions/monitoractions", acts);
    s.sync();
    this->updateView();
}

void MonitorActionsDialog::handleEditAction()
{
    QList<QListWidgetItem*> selection = this->list_view->selectedItems();
    QListWidgetItem *item = selection.at(0);
    QString name = item->data(Qt::DisplayRole).toString();
    QSettings s;
    QHash<QString, QVariant> acts = s.value("actions/monitoractions").toHash();
    QHash<QString, QVariant> targetConf = acts.value(this->target).toHash();
    QHash<QString, QVariant> actionConf = targetConf.value(name).toHash();

    MonitorActionCreate create(name, actionConf, this);

    if (create.exec() == QDialog::Rejected) return;

    targetConf.remove(name);

    QString cmd  = create.cmd->text();
    QString args = create.args->text();
    QString newname = create.name->text();

    QHash<QString, QVariant> newActionConf;
    newActionConf.insert("cmd", QVariant(cmd));
    newActionConf.insert("args", QVariant(args));
    targetConf.insert(newname, QVariant(newActionConf));
    acts.insert(this->target, QVariant(targetConf));
    s.setValue("actions/monitoractions", acts);
    s.sync();
    this->updateView();
}

void MonitorActionsDialog::handleSelectionChange()
{
    QList<QListWidgetItem*> selection = this->list_view->selectedItems();
    if (selection.size() == 0) {
        this->delAction->setDisabled(true);
        this->editAction->setDisabled(true);
    } else {
        this->delAction->setDisabled(false);
        this->editAction->setDisabled(false);
    }

}

void MonitorActionsDialog::handleAddAction()
{
    MonitorActionCreate create(this);

    if (create.exec() == QDialog::Rejected) return;

    QString cmd = create.cmd->text();
    QString args = create.args->text();
    QString name = create.name->text();
    qDebug() << "should create action: " << cmd << args << name;

    QSettings s;
    QHash<QString, QVariant> acts = s.value("actions/monitoractions").toHash();
    QVariant var = acts.value(this->target);

    QHash<QString, QVariant> targetConf;

    if (var.isValid()) {
        qDebug() << "valid";
        targetConf = var.toHash();
    } else {
        qDebug() << "invalid";
    }
    QHash<QString, QVariant> actionConf;
    actionConf.insert("cmd", QVariant(cmd));
    actionConf.insert("args", QVariant(args));
    targetConf.insert(name, QVariant(actionConf));

    qDebug() << "not variant:" << targetConf;
    QVariant targetConfVar = QVariant(targetConf);
    qDebug() << "variant variant:" << targetConfVar;
    acts.insert(this->target, targetConfVar);
    s.setValue("actions/monitoractions", acts);
    s.sync();
    this->updateView();
}
