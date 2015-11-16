#ifndef MONITORWIDGET_H
#define MONITORWIDGET_H

#include "include/nframe.h"
#include "include/nframecontainer.h"
#include "include/ngrid.h"
#include "include/ngridcontainer.h"
#include "include/dialogs/newtarget.h"
#include "include/dialogs/newprobe.h"
#include "include/network/supercast.h"
#include "include/network/supercastsignal.h"
#include "include/monitor/treeview.h"
#include "include/monitor/nchecks.h"
#include "include/monitor/monitor.h"
#include "include/monitor/monitorlogs.h"
#include "include/statusbuttonwidget.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QPushButton>
#include <QLineEdit>
#include <QIcon>
#include <QMap>
#include <QDesktopServices>
#include <QUrl>
#include <QPalette>
#include <QPixmap>

#include <QDebug>

class MonitorWidget : public NFrameContainer
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