#ifndef MONITOR_H
#define MONITOR_H

#include "nframe.h"
#include "nframecontainer.h"
#include "ngrid.h"
#include "ngridcontainer.h"
#include "monitor_tree/treeview.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QPushButton>
#include <QLineEdit>
#include <QIcon>

class Monitor : public NFrame
{
public:
    Monitor(QWidget *parent = 0);
};

#endif // MONITOR_H
