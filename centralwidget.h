#ifndef CENTRALWIDGET_H
#define CENTRALWIDGET_H

#include "ngrid.h"
#include "ngridcontainer.h"
#include "nframe.h"
#include "nframecontainer.h"
#include "sidebutton.h"
#include "monitor.h"
#include "dashboard.h"

#include <QObject>
#include <QWidget>
#include <QGridLayout>
#include <QLabel>
#include <QButtonGroup>
#include <QStackedLayout>

class CentralWidget : public NFrame
{
public:
    CentralWidget(QWidget *parent = 0);
    static const int MONITOR   = 0;
    static const int DASHBOARD = 1;
};

#endif // CENTRALWIDGET_H
