#ifndef DASHBOARD_H
#define DASHBOARD_H

#include "nframecontainer.h"
#include "ngrid.h"

#include <QObject>
#include <QWidget>
#include <QLabel>

class Dashboard : public NFrameContainer
{
public:
    Dashboard(QWidget *parent = 0);
};

#endif // DASHBOARD_H
