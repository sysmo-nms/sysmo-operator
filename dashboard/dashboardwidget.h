#ifndef DASHBOARDWIDGET_H
#define DASHBOARDWIDGET_H

#include "nframe.h"
#include "ngridcontainer.h"
#include "dashboardtab.h"

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
