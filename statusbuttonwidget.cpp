#include "statusbuttonwidget.h"

StatusButtonWidget::StatusButtonWidget(QWidget* parent) :
    NFrameContainer(parent)
{
    NGridContainer* grid = new NGridContainer();
    this->setLayout(grid);

    StatusButton* okButton   = new StatusButton(this, "OK",
                                              QPixmap(":/icons/weather-clear"));
    StatusButton* errButton  = new StatusButton(this, "ERROR",
                                   QPixmap(":/icons/weather-few-clouds-night"));
    StatusButton* warnButton = new StatusButton(this, "WARNING",
                                            QPixmap(":/icons/weather-showers"));
    StatusButton* critButton = new StatusButton(this, "CRITICAL",
                                       QPixmap(":/icons/weather-severe-alert"));
    grid->addWidget(okButton,   0,0);
    grid->addWidget(errButton,  1,0);
    grid->addWidget(warnButton, 2,0);
    grid->addWidget(critButton, 3,0);
    this->setFixedWidth(100);
}

