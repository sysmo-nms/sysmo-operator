#ifndef MONITOR_H
#define MONITOR_H

#include "nframecontainer.h"
#include "ngrid.h"

#include <QObject>
#include <QWidget>
#include <QLabel>

class Monitor : public NFrameContainer
{
public:
    Monitor(QWidget *parent = 0);
};

#endif // MONITOR_H
