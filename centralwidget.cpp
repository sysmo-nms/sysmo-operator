#include "centralwidget.h"

CentralWidget::CentralWidget(QWidget *parent)
   : NFrame(parent)
{
    QLabel *lab = new QLabel(this);
    lab->setText(QString("hello"));

    NGrid *grid = new NGrid();
    grid->setHorizontalSpacing(6);
    grid->setVerticalSpacing(6);
    grid->addWidget(lab, 0, 0);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);

    this->setLayout(grid);
}
