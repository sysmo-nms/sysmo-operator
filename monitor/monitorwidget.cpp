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

    // timeline panel
    NFrame* timelineFrame = new NFrame(this);
    timelineFrame->setFixedHeight(173);
    NGrid* tgrid = new NGrid();
    timelineFrame->setLayout(tgrid);
    timelineFrame->setFrameShape(QFrame::StyledPanel);

    MonitorLogs* timeline = new MonitorLogs(this);
    StatusButtonWidget* statusBox = new StatusButtonWidget(this);
    //timeline->setBackgroundRole(QPalette::AlternateBase);
    //timeline->setAutoFillBackground(true);
    tgrid->addWidget(timeline, 0,1);
    tgrid->addWidget(statusBox, 0,0);
    tgrid->setColumnStretch(0,0);
    tgrid->setColumnStretch(1,1);

    // tree frame
    NFrame* treeFrame = new NFrame(this);
    treeFrame->setFrameShape(QFrame::StyledPanel);
    NGrid* treegrid = new NGrid();
    treegrid->setVerticalSpacing(4);
    treeFrame->setLayout(treegrid);

    NGridContainer* container = new NGridContainer();
    container->setVerticalSpacing(2);
    container->setHorizontalSpacing(2);
    //container->addWidget(controlFrame, 0,0);
    container->addWidget(treeFrame, 0,0);
    container->addWidget(timelineFrame, 1,0);
    container->setRowStretch(0,1);
    container->setRowStretch(1,0);
    this->setLayout(container);

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
    QObject::connect(
                statusBox->ok, SIGNAL(setText(QString)),
                search, SLOT(setText(QString)));
    QObject::connect(
                statusBox->err, SIGNAL(setText(QString)),
                search, SLOT(setText(QString)));
    QObject::connect(
                statusBox->crit, SIGNAL(setText(QString)),
                search, SLOT(setText(QString)));
    QObject::connect(
                statusBox->warn, SIGNAL(setText(QString)),
                search, SLOT(setText(QString)));



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
    QObject::connect(
                this->mon, SIGNAL(initialSyncEnd()),
                tree, SLOT(initialSyncEnd()));

    // new probe dialog connect
    QObject::connect(
                tree->target_menu, SIGNAL(openNewProbeDialog(QString)),
                this,              SLOT(showNewProbeDialog(QString)));


    /*
    MonitorLogs* monlog = new MonitorLogs(this);

    QObject::connect(
                this->mon, SIGNAL(probeReturn(QVariant)),
                monlog, SLOT(probeReturn(QVariant)));
                */

    /*
     * right layout
     */
    treegrid->addWidget(create, 0,0);
    treegrid->addWidget(search_clear,  0,1);
    treegrid->addWidget(help, 0,3);
    treegrid->addWidget(tree,   1,0,1,4);
    treegrid->setColumnStretch(0,0);
    treegrid->setColumnStretch(1,0);
    treegrid->setColumnStretch(2,3);
    treegrid->setRowStretch(0,0);
    treegrid->setRowStretch(1,1);

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
                sig, SIGNAL(serverMessage(QVariant)),
                this->mon, SLOT(handleServerMessage(QVariant)));

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
