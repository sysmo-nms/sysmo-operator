#include "monitorwidget.h"

MonitorWidget*                   MonitorWidget::singleton  = NULL;
QMap<QString,QJsonObject>* MonitorWidget::target_map = NULL;
QMap<QString,QJsonObject>* MonitorWidget::probe_map  = NULL;

MonitorWidget* MonitorWidget::getInstance() {return MonitorWidget::singleton;}

MonitorWidget::MonitorWidget(QWidget* parent) : NFrame(parent)
{
    MonitorWidget::target_map = new QMap<QString, QJsonObject>();
    MonitorWidget::probe_map  = new QMap<QString, QJsonObject>();

    MonitorWidget::singleton = this;
    this->setFrameShape(QFrame::StyledPanel);
    NGrid* grid = new NGrid();
    grid->setVerticalSpacing(4);
    this->setLayout(grid);

    // top controls
    QPushButton* create = new QPushButton(this);
    create->setIcon(QIcon(":/icons/list-add.png"));
    create->setWhatsThis("Click this button to add new targets host.");
    create->setStatusTip("Create a new target.");
    QObject::connect(
                create, SIGNAL(clicked(bool)),
                this,   SLOT(newTarget()));
    QPushButton* clear  = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));
    QLineEdit*   search = new QLineEdit(this);
    search->setFixedWidth(250);
    QObject::connect(
                clear, SIGNAL(pressed()),
                search, SLOT(clear()));

    // clear/search layout
    NFrameContainer* search_clear      = new NFrameContainer(this);
    NGridContainer*  search_clear_grid = new NGridContainer();
    search_clear->setLayout(search_clear_grid);
    search_clear_grid->addWidget(clear, 0,0);
    search_clear_grid->addWidget(search,  0,1);
    search_clear_grid->setColumnStretch(0,0);
    search_clear_grid->setColumnStretch(1,1);
    search_clear_grid->setHorizontalSpacing(4);

    // help button
    QPushButton* help = new QPushButton(this);
    help->setIcon(QIcon(":/icons/dialog-information.png"));
    help->setFlat(true);

    // treeview
    TreeView* tree = new TreeView(this);

    QObject::connect(
                search,
                        SIGNAL(textChanged(QString)),
                tree->filter_model,
                        SLOT(setFilterFixedString(QString)));
    QObject::connect(
                search,
                        SIGNAL(textChanged(QString)),
                tree,   SLOT(expandAll()));

    // new probe dialog connect
    QObject::connect(
                tree->target_menu, SIGNAL(openNewProbeDialog(QString)),
                this, SLOT(newProbe(QString)));

    grid->addWidget(create, 0,0);
    grid->addWidget(search_clear,  0,1);
    grid->addWidget(help, 0,3);
    grid->addWidget(tree,   1,0,1,4);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,0);
    grid->setColumnStretch(2,1);
    grid->setColumnStretch(3,0);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);

    // get a NewTarget instance
    this->add_target_dialog = new NewTarget(this);
    this->add_probe_dialog  = new NewProbe(this);

    // supercast init
    SupercastSignal* sig = new SupercastSignal(this);
    QObject::connect(
                sig,	SIGNAL(sendMessage(QJsonObject)),
                this,	SLOT(handleServerMessage(QJsonObject)));
    Supercast::setMessageProcessor(QString("monitor"), sig);
}


MonitorWidget::~MonitorWidget()
{
    delete MonitorWidget::target_map;
    delete MonitorWidget::probe_map;
    /*
     * Save state
     */
}


void MonitorWidget::handleServerMessage(QJsonObject message)
{
    QString     type = message.value("type").toString("undefined");
    QJsonValue  mvalues(message.value("value"));
    QJsonObject mcontent = mvalues.toObject();

    if (type == "infoTarget") {
        QString	    tname(mcontent.value("name").toString(""));

        MonitorWidget::target_map->insert(tname,mcontent);
        emit this->infoTarget(mcontent);


    } else if (type == "infoProbe") {
        QString	    pname(mcontent.value("name").toString(""));

        MonitorWidget::probe_map->insert(pname, mcontent);
        emit this->infoProbe(mcontent);


    } else if (type == "deleteTarget") {
        QString	    tname(mcontent.value("name").toString(""));

        MonitorWidget::target_map->remove(tname);
        emit this->deleteTarget(mcontent);


    } else if (type == "deleteProbe") {
        QString	    pname(mcontent.value("name").toString(""));

        MonitorWidget::target_map->remove(pname);
        emit this->deleteProbe(mcontent);


    } else if (type == "probeReturn") {
        emit this->probeReturn(mcontent);


    } else if (type == "nchecksSimpleDumpMessage") {
    } else if (type == "nchecksSimpleUpdateMessage") {
    } else if (type == "nchecksTableDumpMessage") {
    } else if (type == "nchecksTableUpdateMessage") {
    } else if (type == "subscribeOk") {
    } else if (type == "unSubscribeOk") {
    } else {
        QJsonDocument doc(message);
        qDebug() << "received message!!" << type;
        qDebug() << doc.toJson();
   }
}


void MonitorWidget::connexionStatus(int status)
{
    if (status == Supercast::ConnexionSuccess) {
        Supercast::subscribe("target-MasterChan");
    } else {
        TreeView* tree = this->findChild<TreeView *>("MonitorTreeView");
        tree->stopTimer();
        // the application is in an error state.
        this->add_target_dialog->hide();
    }
}


void MonitorWidget::newTarget()
{
    this->add_target_dialog->show();
}

void MonitorWidget::newProbe(QString forTarget)
{
    this->add_probe_dialog->setTarget(forTarget);
    this->add_probe_dialog->show();

}
