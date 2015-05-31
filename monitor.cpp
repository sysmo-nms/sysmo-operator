#include "monitor.h"

Monitor::Monitor(QWidget *parent)
        : NFrame(parent)
{
    this->setFrameShape(QFrame::StyledPanel);
    NGrid *grid = new NGrid();
    grid->setVerticalSpacing(4);
    this->setLayout(grid);

    // top controls
    QPushButton *create = new QPushButton(this);
    QPushButton *clear  = new QPushButton(this);
    create->setIcon(QIcon(":/ressources/list-add32.png"));
    clear->setIcon(QIcon(":/ressources/edit-clear32.png"));
    QLineEdit   *search = new QLineEdit(this);
    search->setFixedWidth(250);

    // clear/search layout
    NFrameContainer *search_clear = new NFrameContainer(this);
    NGridContainer  *search_clear_grid = new NGridContainer();
    search_clear->setLayout(search_clear_grid);
    search_clear_grid->addWidget(clear, 0,0);
    search_clear_grid->addWidget(search,  0,1);
    search_clear_grid->setColumnStretch(0,0);
    search_clear_grid->setColumnStretch(1,1);
    search_clear_grid->setHorizontalSpacing(4);

    // help button
    QPushButton *help = new QPushButton(this);
    help->setIcon(QIcon(":/ressources/images/32/dialog-information.png"));
    help->setFlat(true);

    // treeview
    TreeView *tree = new TreeView(this);

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

