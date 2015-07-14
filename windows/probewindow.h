#ifndef PROBEWINDOW_H
#define PROBEWINDOW_H

#include "nframecontainer.h"
#include "ngridcontainer.h"
#include "ngrid.h"
#include "nframe.h"
#include "monitor/monitor.h"
#include "monitor/monitorproxywidget.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QCloseEvent>
#include <QHash>
#include <QCoreApplication>
#include <QApplication>
#include <QStatusBar>
#include <QPalette>
#include <QComboBox>
#include <QScrollArea>
#include <QJsonObject>

#include <QDebug>

class ProbeWindow : public MonitorProxyWidget
{
    Q_OBJECT
private:
    ProbeWindow(QString probeName);
    ~ProbeWindow();
    QString name = "";
    static QHash<QString, ProbeWindow*> windows;
    QStatusBar* status_bar = NULL;

public:
    static void openWindow(QString name);
    void handleEvent(QJsonObject event);

signals:

public slots:
    void closeEvent(QCloseEvent* event);
};

#endif // PROBEWINDOW_H
