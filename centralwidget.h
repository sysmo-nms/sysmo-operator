#ifndef CENTRALWIDGET_H
#define CENTRALWIDGET_H

#include "ngrid.h"
#include "ngridcontainer.h"
#include "nframe.h"
#include "nframecontainer.h"
#include "sidebutton.h"
#include "monitor/monitorwidget.h"
#include "dashboard/dashboardwidget.h"

#include <QObject>
#include <QWidget>
#include <QGridLayout>
#include <QLabel>
#include <QButtonGroup>
#include <QStackedLayout>
#include <QSize>
#include <QIcon>

class CentralWidget : public NFrameContainer
{
    Q_OBJECT

public:
    explicit CentralWidget(QWidget* parent = 0);
    static const int MonitorApp   = 0;
    static const int DashboardApp = 1;
};

#endif // CENTRALWIDGET_H
