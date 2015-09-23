#ifndef MONITORWIDGET_H
#define MONITORWIDGET_H

#include "nframe.h"
#include "nframecontainer.h"
#include "ngrid.h"
#include "ngridcontainer.h"
#include "dialogs/newtarget.h"
#include "dialogs/newprobe.h"
#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "monitor/treeview.h"
#include "monitor/nchecks.h"
#include "monitor/monitor.h"
#include "monitor/monitorlogs.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QPushButton>
#include <QLineEdit>
#include <QIcon>
#include <QMap>
#include <QJsonObject>
#include <QJsonDocument>
#include <QDesktopServices>
#include <QUrl>

#include <QDebug>

class MonitorWidget : public NFrame
{
    Q_OBJECT

public:
    explicit MonitorWidget(QWidget* parent = 0);
    ~MonitorWidget();
    NewProbe*  add_probe_dialog;
    static MonitorWidget* getInstance();

public slots:
    void showNewTargetDialog();
    void showNewProbeDialog(QString forTarget);
    void connectionStatus(int status);
    void handleHelpClicked();

private:
    static MonitorWidget* singleton;
    Monitor* mon;
};

#endif // MONITORWIDGET_H
