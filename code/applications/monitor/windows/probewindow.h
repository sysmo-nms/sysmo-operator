/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

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
#include <widgets/nowheelcombobox.h>

#include <QString>
#include <QMap>
#include <QVariant>
#include <QStatusBar>
#include <QScrollArea>
#include <QTimer>
#include <QResizeEvent>
#include <QCloseEvent>

#include <applications/monitor/monitor.h>
#include <widgets/nframecontainer.h>

class ProbeWindow : public MonitorProxyWidget {
    Q_OBJECT
private:
    ProbeWindow(QString probeName);
    ~ProbeWindow();

    QString name;
    QMap<QString, QVariant> rrd_config;
    QMap<QString, QVariant> target;

    QStatusBar* status_bar;
    QScrollArea* scroll_area;
    NoWheelComboBox* height_cbox;
    NoWheelComboBox* time_span_cbox;
    QTimer* timer;
    int divider;
    int margin;
    int h_margin;
    int graphs_number;
    NFrameContainer* log_area;
    void resizeEvent(QResizeEvent *event);

    static QMap<QString, ProbeWindow*> windows;
    void restoreStateFromSettings();
    void triggerRedraw();
    int getOptimalHeight();

public:
    static void openWindow(QString name);
    void handleEvent(QVariant event);

    static int getSpanFor(int value);
    static const int SPAN_TWO_HOURS = 0;
    static const int SPAN_TWELVE_HOURS = 1;
    static const int SPAN_TWO_DAYS = 2;
    static const int SPAN_SEVEN_DAYS = 3;
    static const int SPAN_TWO_WEEKS = 4;
    static const int SPAN_ONE_MONTH = 5;
    static const int SPAN_SIX_MONTH = 6;
    static const int SPAN_ONE_YEAR = 7;
    static const int SPAN_THREE_YEARS = 8;
    static const int SPAN_TEN_YEARS = 9;

    static bool isThumbnail(int value);
    static const int HEIGHT_SMALL = 0;
    static const int HEIGHT_NORMAL = 1;
    static const int HEIGHT_LARGE = 2;
    static const int HEIGHT_AUTO = 3;
    int getHeightFor(int value);


public slots:
    void handleSpanChanged();
    void handleHeightChanged();
    void handleTimerTimeout();

signals:
    void graphConfigChanged(int width, int height, int span);

public slots:
    void closeEvent(QCloseEvent* event);
};

#endif // PROBEWINDOW_H
