#ifndef DASHBOARD_H
#define DASHBOARD_H

#include "nframe.h"
#include "ngrid.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>

class Dashboard : public NFrame
{
public:
    Dashboard(QWidget *parent = 0);
};

#endif // DASHBOARD_H
