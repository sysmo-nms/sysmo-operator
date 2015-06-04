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
#include "network/supercastsignal.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QPushButton>
#include <QLineEdit>
#include <QIcon>
#include <QMap>
#include <QJsonObject>

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
    void handleServerMessage(QJsonObject message);

private:
    static Monitor* singleton;
    QMap<QString, QJsonObject>* target_map;
    QMap<QString, QJsonObject>* probe_map;
};

#endif // MONITOR_H
