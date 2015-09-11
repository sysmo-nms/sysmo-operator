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
#include <QPalette>
#include <QSettings>
#include <QVariant>

#include <QDebug>

class ProbeWindow : public MonitorProxyWidget
{
    Q_OBJECT
private:
    ProbeWindow(QString probeName);
    ~ProbeWindow();

    QString     name;
    QJsonObject rrd_config;
    QJsonObject target;

    QStatusBar*    status_bar;
    QScrollArea*  scroll_area;
    NoWheelComboBox* height_cbox;
    QTimer* timer;
    int divider;
    int margin;
    void resizeEvent(QResizeEvent *event);

    static QHash<QString, ProbeWindow*> windows;
    void restoreStateFromSettings();

public:
    static void openWindow(QString name);
    void handleEvent(QJsonObject event);

    static int getSpanFor(int value);
    static const int SPAN_TWO_HOURS     = 0;
    static const int SPAN_TWELVE_HOURS  = 1;
    static const int SPAN_TWO_DAYS      = 2;
    static const int SPAN_SEVEN_DAYS    = 3;
    static const int SPAN_TWO_WEEKS     = 4;
    static const int SPAN_ONE_MONTH     = 5;
    static const int SPAN_SIX_MONTH     = 6;
    static const int SPAN_ONE_YEAR      = 7;
    static const int SPAN_THREE_YEARS   = 8;
    static const int SPAN_TEN_YEARS     = 9;

    static bool isThumbnail(int value);
    static int getHeightFor(int value);
    static const int HEIGHT_SMALL       = 0;
    static const int HEIGHT_NORMAL      = 1;
    static const int HEIGHT_LARGE       = 2;


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
