#include "monitor.h"

Monitor*                   Monitor::singleton  = NULL;
QMap<QString,QJsonObject>* Monitor::target_map = NULL;
QMap<QString,QJsonObject>* Monitor::probe_map  = NULL;

Monitor* Monitor::getInstance() {return Monitor::singleton;}

Monitor::Monitor(QWidget* parent) : NFrame(parent)
{
    Monitor::target_map = new QMap<QString, QJsonObject>();
    Monitor::probe_map  = new QMap<QString, QJsonObject>();

    Monitor::singleton = this;
    this->setFrameShape(QFrame::StyledPanel);
    NGrid* grid = new NGrid();
    grid->setVerticalSpacing(4);
    this->setLayout(grid);

    // top controls
    QPushButton* create = new QPushButton(this);
    create->setIcon(QIcon(":/icons/list-add.png"));
    QObject::connect(
                create, SIGNAL(clicked(bool)),
                this,   SLOT(newTarget()));
    QPushButton* clear  = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));
    QLineEdit*   search = new QLineEdit(this);
    search->setFixedWidth(250);

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

    // supercast init
    SupercastSignal* sig = new SupercastSignal(this);
    QObject::connect(
                sig,	SIGNAL(sendMessage(QJsonObject)),
                this,	SLOT(handleServerMessage(QJsonObject)));
    Supercast::setMessageProcessor(QString("monitor"), sig);
}


Monitor::~Monitor()
{
    /*
     * Save state
     */
}


void Monitor::handleServerMessage(QJsonObject message)
{
    QString     type = message.value("type").toString("undefined");
    QJsonValue  mvalues(message.value("value"));
    QJsonObject mcontent = mvalues.toObject();

    if (type == "infoTarget") {
        QString	    tname(mcontent.value("name").toString(""));

        Monitor::target_map->insert(tname,mcontent);
        emit this->infoTarget(mcontent);


    } else if (type == "infoProbe") {
        QString	    pname(mcontent.value("name").toString(""));

        Monitor::probe_map->insert(pname, mcontent);
        emit this->infoProbe(mcontent);


    } else if (type == "deleteTarget") {
        QString	    tname(mcontent.value("name").toString(""));

        Monitor::target_map->remove(tname);
        emit this->deleteProbe(mcontent);


    } else if (type == "deleteProbe") {
        QString	    pname(mcontent.value("name").toString(""));

        Monitor::target_map->remove(pname);
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
        std::cout << "received message!!" << type.toStdString() << std::endl;
        std::cout << doc.toJson().toStdString() << std::endl;
   }
}


void Monitor::connexionStatus(int status)
{
    if (status == Supercast::ConnexionSuccess) {
        Supercast::subscribe("target-MasterChan");
    } else {
        // the application is in an error state.
        this->add_target_dialog->hide();
        this->setDisabled(true);
    }
}


void Monitor::newTarget()
{
    this->add_target_dialog->show();
}
