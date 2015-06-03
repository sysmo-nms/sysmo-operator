#ifndef MONITOR_H
#define MONITOR_H

#include "iostream"

#include "nframe.h"
#include "nframecontainer.h"
#include "ngrid.h"
#include "ngridcontainer.h"
#include "dialogs/newtarget.h"
#include "monitor_tree/treeview.h"
#include "network/supercast.h"

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
    explicit Monitor(QWidget* parent = 0);
    ~Monitor();
    NewTarget* add_target_dialog;
    static Monitor* getInstance();

public slots:
    void newTarget();
    void connexionStatus(int status);

private:
    static Monitor* singleton;
};

#endif // MONITOR_H
