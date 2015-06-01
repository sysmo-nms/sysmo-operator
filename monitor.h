#ifndef MONITOR_H
#define MONITOR_H

#include "nframe.h"
#include "nframecontainer.h"
#include "ngrid.h"
#include "ngridcontainer.h"
#include "dialogs/newtarget.h"
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
    Q_OBJECT

public:
    explicit Monitor(QWidget *parent = 0);
    NewTarget *new_target_dialog;

public slots:
    void newTarget();
};

#endif // MONITOR_H
