/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
#ifndef PROBEWINDOW_H
#define PROBEWINDOW_H

#include "../nframecontainer.h"
#include "../ngridcontainer.h"
#include "../ngrid.h"
#include "../nframe.h"
#include "../monitor/monitor.h"
#include "../monitor/nchecks.h"
#include "../monitor/xml/parsecheckmakegraphcmd.h"
#include "../rrds/rrd4qtgraph.h"
#include "../nowheelcombobox.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QFrame>
#include <QCloseEvent>
#include <QMap>
#include <QCoreApplication>
#include <QApplication>
#include <QStatusBar>
#include <QScrollArea>
#include <QPalette>
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
    QMap<QString,QVariant> rrd_config;
    QMap<QString,QVariant> target;

    QStatusBar*    status_bar;
    QScrollArea*  scroll_area;
    NoWheelComboBox* height_cbox;
    QTimer* timer;
    int divider;
    int margin;
    void resizeEvent(QResizeEvent *event);

    static QMap<QString, ProbeWindow*> windows;
    void restoreStateFromSettings();

public:
    static void openWindow(QString name);
    void handleEvent(QVariant event);

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
