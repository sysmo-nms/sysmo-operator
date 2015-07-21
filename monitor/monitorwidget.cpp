#include "monitorwidget.h"

MonitorWidget* MonitorWidget::singleton  = NULL;
MonitorWidget* MonitorWidget::getInstance() {return MonitorWidget::singleton;}

MonitorWidget::MonitorWidget(QWidget* parent) : NFrame(parent)
{
    MonitorWidget::singleton = this;

    /*
     * Initialize utils first
     */
    this->mon = new Monitor(this);
    new NChecks(this);



    /*
     * init layout
     */
    this->setFrameShape(QFrame::StyledPanel);
    NGrid* grid = new NGrid();
    grid->setVerticalSpacing(4);
    this->setLayout(grid);


    /*
     * top controls
     */
    QPushButton* create = new QPushButton(this);
    create->setIcon(QIcon(":/icons/list-add.png"));
    create->setStatusTip("Create a new target.");
    QObject::connect(
                create, SIGNAL(clicked(bool)),
                this,   SLOT(showNewTargetDialog()));
    QPushButton* clear  = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));
    clear->setStatusTip("Clear filter line");
    QLineEdit*   search = new QLineEdit(this);
    search->setFixedWidth(250);
    search->setStatusTip("Filter the target/probe view");
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


    /*
     * treeview
     */
    TreeView* tree = new TreeView(this);

    QObject::connect(
                clear, SIGNAL(clicked(bool)),
                tree, SLOT(clearSelection()));
    QObject::connect(
                search,             SIGNAL(textChanged(QString)),
                tree->filter_model, SLOT(setFilterFixedString(QString)));
    QObject::connect(
                search, SIGNAL(textChanged(QString)),
                tree,   SLOT(expandAll()));

    // new probe dialog connect
    QObject::connect(
                tree->target_menu, SIGNAL(openNewProbeDialog(QString)),
                this,              SLOT(showNewProbeDialog(QString)));


    /*
     * layout
     */
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

}


MonitorWidget::~MonitorWidget()
{
    /*
     * Save state
     */
}


void MonitorWidget::connectionStatus(int status)
{

    if (status == Supercast::CONNECTION_SUCCESS) {
        SupercastSignal* sig = new SupercastSignal(this);
        QObject::connect(
                sig, SIGNAL(serverMessage(QJsonObject)),
                this->mon, SLOT(handleServerMessage(QJsonObject)));
        Supercast::subscribe("monitor_main", sig);
    } else {
        // the application is in an error state.
        TreeView* tree = this->findChild<TreeView *>("MonitorTreeView");
        tree->stopTimer();

    }
}


/*
 * Dialogs will open at the center of the application when launched
 * from a central widget, wich is the case for MonitorWidget.
 */
void MonitorWidget::showNewTargetDialog()
{
    NewTarget* tdial = new NewTarget(this);
    tdial->exec();
    tdial->deleteLater();
}

void MonitorWidget::showNewProbeDialog(QString forTarget)
{
    NewProbe* pdial = new NewProbe(forTarget, this);
    pdial->exec();
    pdial->deleteLater();
}
