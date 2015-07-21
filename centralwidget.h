#ifndef CENTRALWIDGET_H
#define CENTRALWIDGET_H

#include "ngrid.h"
#include "ngridcontainer.h"
#include "nframecontainer.h"
#include "sidebutton.h"
#include "monitor/monitorwidget.h"
#include "dashboard/dashboardwidget.h"

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
