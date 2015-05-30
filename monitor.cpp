#include "monitor.h"

Monitor::Monitor(QWidget *parent)
        : NFrameContainer(parent)
{
    NGrid *grid = new NGrid();
    this->setLayout(grid);
    QLabel *lab = new QLabel("hello monitor", this);
    grid->addWidget(lab);
}

