#ifndef DASHBOARDWIDGET_H
#define DASHBOARDWIDGET_H

#include "include/nframe.h"
#include "include/ngridcontainer.h"
#include "include/dashboard/dashboardtab.h"

#include <QObject>
#include <QWidget>
#include <QTabWidget>
#include <QTabBar>
#include <QLabel>
#include <QPushButton>
#include <QIcon>


class DashboardWidget : public NFrame
{
    Q_OBJECT

public:
    explicit DashboardWidget(QWidget* parent = 0);
    ~DashboardWidget();
};

#endif // DASHBOARDWIDGET_H
