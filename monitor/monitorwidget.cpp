#include "monitorwidget.h"

MonitorWidget* MonitorWidget::singleton  = NULL;
MonitorWidget* MonitorWidget::getInstance() {return MonitorWidget::singleton;}

MonitorWidget::MonitorWidget(QWidget* parent) : NFrameContainer(parent)
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
    NGridContainer* container = new NGridContainer();
    container->setVerticalSpacing(2);
    this->setLayout(container);

    // left panel
    NFrame* bottomFrame = new NFrame(this);
    NGrid* lgrid = new NGrid();
    bottomFrame->setLayout(lgrid);
    bottomFrame->setFrameShape(QFrame::StyledPanel);
    StatusButtonWidget* statusBox = new StatusButtonWidget(this);

    NFrame* timeline = new NFrame(this);
    timeline->setBackgroundRole(QPalette::AlternateBase);
    timeline->setAutoFillBackground(true);


    /*
    //timeline to left
    lgrid->setRowStretch(1,1);
    lgrid->setRowStretch(0,0);
    lgrid->addWidget(statusBox, 0,0);
    lgrid->addWidget(timeline, 1,0);
    */

    // timeline to bottom
    lgrid->setColumnStretch(0,0);
    lgrid->setColumnStretch(1,1);
    lgrid->addWidget(statusBox, 0,0);
    lgrid->addWidget(timeline, 0,1);


    // right frame
    NFrame* topFrame = new NFrame(this);
    topFrame->setFrameShape(QFrame::StyledPanel);
    NGrid* rgrid = new NGrid();
    rgrid->setVerticalSpacing(4);
    topFrame->setLayout(rgrid);

    //timeline to bottom
    container->setRowStretch(0,1);
    container->setRowStretch(1,0);
    container->addWidget(topFrame, 0,0);
    container->addWidget(bottomFrame,1,0);

    /*
    //timeline to left
    container->setColumnStretch(0,0);
    container->setColumnStretch(1,1);
    container->addWidget(bottomFrame,0,0);
    container->addWidget(topFrame,0,1);
    */

    /*
     * top controls
     */
    QPushButton* create = new QPushButton(this);
    create->setIcon(QIcon(":/icons/list-add.png"));
    create->setStatusTip("Create a new target.");
    QObject::connect(
                create, SIGNAL(clicked(bool)),
                this,   SLOT(showNewTargetDialog()));

    QPushButton* clear = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));
    clear->setStatusTip("Clear filter line");

    QLineEdit* search = new QLineEdit(this);
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
    help->setIcon(QIcon(":/icons/help-browser.png"));
    help->setFlat(true);
    help->setToolTip("Get help...");
    QObject::connect(
                help, SIGNAL(clicked(bool)),
                this, SLOT(handleHelpClicked()));


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
    QObject::connect(
                tree->add_target_action, SIGNAL(triggered(bool)),
                this, SLOT(showNewTargetDialog()));

    // new probe dialog connect
    QObject::connect(
                tree->target_menu, SIGNAL(openNewProbeDialog(QString)),
                this,              SLOT(showNewProbeDialog(QString)));


    /*
    MonitorLogs* monlog = new MonitorLogs(this);

    QObject::connect(
                this->mon, SIGNAL(probeReturn(QJsonObject)),
                monlog, SLOT(probeReturn(QJsonObject)));
                */

    /*
     * right layout
     */
    rgrid->addWidget(create, 0,0);
    rgrid->addWidget(search_clear,  0,1);
    rgrid->addWidget(help, 0,3);
    rgrid->addWidget(tree,   1,0,1,4);
    //rgrid->addWidget(monlog, 2,0,1,4);
    rgrid->setColumnStretch(0,0);
    rgrid->setColumnStretch(1,0);
    rgrid->setColumnStretch(2,3);
    //grid->setColumnStretch(3,1);
    rgrid->setRowStretch(0,0);
    rgrid->setRowStretch(1,1);

}


MonitorWidget::~MonitorWidget()
{
    /*
     * Save state
     */
}


void MonitorWidget::connectionStatus(int status)
{

    if (status == Supercast::CONNECTION_SUCCESS)
    {
        SupercastSignal* sig = new SupercastSignal();
        QObject::connect(
                sig, SIGNAL(serverMessage(QJsonObject)),
                this->mon, SLOT(handleServerMessage(QJsonObject)));

        Supercast::subscribe("monitor_main", sig);
    }
    else
    {
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

void MonitorWidget::handleHelpClicked()
{
    QDesktopServices::openUrl(QUrl("http://www.sysmo.io/Community/"));

}
