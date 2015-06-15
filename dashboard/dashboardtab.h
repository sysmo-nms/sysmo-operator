#ifndef DASHBOARDTAB_H
#define DASHBOARDTAB_H

#include "nframecontainer.h"
#include "ngridcontainer.h"
#include "ngrid.h"

#include <QWidget>
#include <QPushButton>
#include <QMdiArea>
#include <QIcon>

class DashboardTab : public NFrameContainer
{
public:
    explicit DashboardTab(QWidget* parent = 0);
};

#endif // DASHBOARDTAB_H
