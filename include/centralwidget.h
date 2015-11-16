#ifndef CENTRALWIDGET_H
#define CENTRALWIDGET_H

#include "include/ngrid.h"
#include "include/ngridcontainer.h"
#include "include/nframecontainer.h"
#include "include/sidebutton.h"
#include "include/monitor/monitorwidget.h"
#include "include/dashboard/dashboardwidget.h"

#include <QObject>
#include <QWidget>
#include <QButtonGroup>
#include <QStackedLayout>
#include <QSize>
#include <QIcon>

class CentralWidget : public NFrameContainer
{

private:
    static const int APP_MONITOR   = 0;
    static const int APP_DASHBOARD = 1;

public:
    explicit CentralWidget(QWidget* parent = 0);
};

#endif // CENTRALWIDGET_H
