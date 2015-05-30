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
    QLineEdit   *search = new QLineEdit(this);
    search->setFixedWidth(250);

    // treeview
    TreeView *tree = new TreeView(this);

    grid->addWidget(create, 0,0);
    grid->addWidget(clear,  0,1);
    grid->addWidget(search, 0,2);
    grid->addWidget(tree,   1,0,1,4);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,0);
    grid->setColumnStretch(2,0);
    grid->setColumnStretch(3,1);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);
}

