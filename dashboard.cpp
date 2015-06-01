#include "dashboard.h"


Dashboard::Dashboard(QWidget *parent) : NFrame(parent)
{
    this->setFrameShape(QFrame::StyledPanel);
    NGrid *grid = new NGrid();
    this->setLayout(grid);
    QLabel *lab = new QLabel("hello dashboard", this);
    grid->addWidget(lab);
}

