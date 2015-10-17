#include "statusbutton.h"

StatusButton::StatusButton(QWidget *parent, QString type, QPixmap pixmap)
        : QPushButton(parent)
{
    this->setFixedHeight(35);
    this->setToolTip(type);
    this->lcd = new QLCDNumber(this);
    this->lcd->setSegmentStyle(QLCDNumber::Flat);
    this->lcd->setFrameShape(QFrame::StyledPanel);
    //this->lcd->setFrameShadow(QFrame::Plain);
    NGrid* grid = new NGrid();

    QLabel* lab = new QLabel(this);
    lab->setPixmap(pixmap);

    //QLabel* labtext = new QLabel(type, this);

    grid->addWidget(lab, 0,0);
    grid->addWidget(this->lcd, 0,1);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    this->setLayout(grid);
}
