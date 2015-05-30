#ifndef MONITOR_H
#define MONITOR_H

#include "nframe.h"
#include "ngrid.h"
#include "monitor_tree/treeview.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QPushButton>
#include <QLineEdit>

class Monitor : public NFrame
{
public:
    Monitor(QWidget *parent = 0);
};

#endif // MONITOR_H
