#ifndef PROBEWINDOW_H
#define PROBEWINDOW_H

#include "nframecontainer.h"
#include "ngridcontainer.h"
#include "ngrid.h"
#include "nframe.h"
#include "monitor/monitor.h"
#include "monitor/nchecks.h"
#include "monitor/xml/parsecheckmakegraphcmd.h"
#include "rrds/rrd4qtgraph.h"

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
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QStringListIterator>

#include <QDebug>

class ProbeWindow : public MonitorProxyWidget
{
    Q_OBJECT
private:
    ProbeWindow(QString probeName);
    ~ProbeWindow();

    QString     name;
    QJsonObject rrd_config;

    QStatusBar*   status_bar = NULL;
    QScrollArea* scroll_area = NULL;

    static QHash<QString, ProbeWindow*> windows;

public:
    static void openWindow(QString name);
    void handleEvent(QJsonObject event);

public slots:
    void closeEvent(QCloseEvent* event);
};

#endif // PROBEWINDOW_H
