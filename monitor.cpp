#include "monitor.h"

Monitor* Monitor::singleton = NULL;
Monitor* Monitor::getInstance() {return Monitor::singleton;}

Monitor::Monitor(QWidget* parent) : NFrame(parent)
{
    Monitor::singleton = this;
    this->setFrameShape(QFrame::StyledPanel);
    NGrid* grid = new NGrid();
    grid->setVerticalSpacing(4);
    this->setLayout(grid);

    // top controls
    QPushButton* create = new QPushButton(this);
    create->setIcon(QIcon(":/ressources/images/32/list-add.png"));
    QObject::connect(
                create, SIGNAL(clicked(bool)),
                this,   SLOT(newTarget()));
    QPushButton* clear  = new QPushButton(this);
    clear->setIcon(QIcon(":/ressources/images/32/edit-clear.png"));
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
    help->setIcon(QIcon(":/ressources/images/32/dialog-information.png"));
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
}


Monitor::~Monitor()
{
    /*
     * Save state
     */
}


void Monitor::connexionStatus(int status)
{
    if (status == Supercast::ConnexionSuccess) {
        // should init myself
        // - connect to supercast
        // - fill treeModel
        std::cout << "initalize myself " << std::endl;
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
