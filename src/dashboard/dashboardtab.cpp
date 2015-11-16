#include "include/dashboard/dashboardtab.h"

DashboardTab::DashboardTab(QWidget* parent) : NFrameContainer(parent)
{
    NGrid* grid = new NGrid();
    this->setLayout(grid);

    NFrameContainer* buttons_container = new NFrameContainer(this);
    NGridContainer*  buttons_layout = new NGridContainer();
    buttons_container->setLayout(buttons_layout);

    QPushButton* button_save   = new QPushButton(this);
    button_save->setIcon(QIcon(":/icons/document-save.png"));
    QPushButton* button_cancel = new QPushButton(this);
    button_cancel->setIcon(QIcon(":/icons/edit-undo.png"));
    buttons_layout->addWidget(button_save,  0,0);
    buttons_layout->addWidget(button_cancel,0,1);
    buttons_layout->setColumnStretch(0,0);
    buttons_layout->setColumnStretch(1,0);
    buttons_layout->setColumnStretch(2,1);

    grid->addWidget(buttons_container, 0,0);

    QMdiArea* mdi = new QMdiArea(this);
    grid->addWidget(mdi, 1, 0);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);
}

