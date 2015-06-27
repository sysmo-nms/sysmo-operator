#include "probewindow.h"

ProbeWindow::ProbeWindow(QString probeName, QWidget* parent)
                        : NFrameContainer(parent)
{
    NGrid* grid = new NGrid();
    this->setLayout(grid);
    grid->addWidget(new QLabel(probeName, this), 0,0);
}
