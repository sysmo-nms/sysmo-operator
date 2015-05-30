#include "dashboard.h"

Dashboard::Dashboard(QWidget *parent)
        : NFrameContainer(parent)
{
    NGrid *grid = new NGrid();
    this->setLayout(grid);
    QLabel *lab = new QLabel("hello dashboard", this);
    grid->addWidget(lab);

}

