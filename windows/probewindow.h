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
#include "nowheelcombobox.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QCloseEvent>
#include <QHash>
#include <QCoreApplication>
#include <QApplication>
#include <QStatusBar>
#include <QScrollArea>
#include <QPalette>
#include <QJsonObject>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QStringListIterator>
#include <QTimer>

#include <QDebug>

class ProbeWindow : public MonitorProxyWidget
{
    Q_OBJECT
private:
    ProbeWindow(QString probeName);
    ~ProbeWindow();

    QString     name;
    QJsonObject rrd_config;

    QStatusBar*    status_bar = NULL;
    QScrollArea*  scroll_area = NULL;
    QTimer* timer = NULL;
    int divider = 1;
    int margin = 150;
    void resizeEvent(QResizeEvent *event);

    static QHash<QString, ProbeWindow*> windows;

public:
    static void openWindow(QString name);
    void handleEvent(QJsonObject event);

    static int getSpanFor(int value);
    static const int SPAN_TWO_HOURS;
    static const int SPAN_TWELVE_HOURS;
    static const int SPAN_TWO_DAYS;
    static const int SPAN_SEVEN_DAYS;
    static const int SPAN_TWO_WEEKS;
    static const int SPAN_ONE_MONTH;
    static const int SPAN_SIX_MONTH;
    static const int SPAN_ONE_YEAR;
    static const int SPAN_THREE_YEARS;
    static const int SPAN_TEN_YEARS;

    static bool isThumbnail(int value);
    static int getHeightFor(int value);
    static const int HEIGHT_THUMBNAIL;
    static const int HEIGHT_SMALL;
    static const int HEIGHT_NORMAL;
    static const int HEIGHT_LARGE;
    static const int HEIGHT_HUGE;


public slots:
    void handleSpanChanged(int span);
    void handleHeightChanged(int height);
    void handleTimerTimeout();

signals:
    void timeSpanChanged(int span);
    void graphHeightChanged(int height);
    void graphWidthChanged(int size);

public slots:
    void closeEvent(QCloseEvent* event);
};

#endif // PROBEWINDOW_H
