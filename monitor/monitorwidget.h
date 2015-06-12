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
#include "monitor/monitor.h"

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

#include <QDebug>

class MonitorWidget : public NFrame
{
    Q_OBJECT

public:
    explicit MonitorWidget(QWidget* parent = 0);
    ~MonitorWidget();
    NewTarget* add_target_dialog = NULL;
    NewProbe*  add_probe_dialog  = NULL;
    static MonitorWidget* getInstance();
    static QMap<QString, QJsonObject>* target_map;
    static QMap<QString, QJsonObject>* probe_map;

public slots:
    void newTarget();
    void newProbe(QString forTarget);
    void connexionStatus(int status);
    void handleServerMessage(QJsonObject message);

private:
    static MonitorWidget* singleton;
    Monitor* monitor = NULL;

signals:
    void infoProbe(QJsonObject message);
    void infoTarget(QJsonObject message);
    void deleteTarget(QJsonObject message);
    void deleteProbe(QJsonObject message);
    void probeReturn(QJsonObject message);
};

#endif // MONITORWIDGET_H
