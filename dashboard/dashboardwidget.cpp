#include "dashboardwidget.h"

DashboardWidget::DashboardWidget(QWidget *parent) : NFrame(parent)
{
    NGridContainer* grid = new NGridContainer();
    this->setLayout(grid);

    QTabWidget* tab = new QTabWidget(this);
    // tabBar() in qt4 is protected
    /*
    QTabBar* tab_bar = tab->tabBar();
    tab_bar->setUsesScrollButtons(true);
    tab_bar->setExpanding(true);
    */

    QPushButton* button_add = new QPushButton(this);
    button_add->setIcon(QIcon(":/icons/list-add.png"));
    button_add->setFlat(true);
    tab->setCornerWidget(button_add, Qt::TopLeftCorner);

    QPushButton* button_help = new QPushButton(this);
    button_help->setIcon(QIcon(":/icons/dialog-information.png"));
    button_help->setFlat(true);
    tab->setCornerWidget(button_help, Qt::TopRightCorner);

    grid->addWidget(tab, 0,0);
    DashboardTab* dash_tab = new DashboardTab(this);
    tab->addTab(dash_tab, "Tab 1");

}

DashboardWidget::~DashboardWidget()
{

}
