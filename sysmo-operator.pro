#-------------------------------------------------
#
# Project created by QtCreator 2015-05-27T17:15:26
#
#-------------------------------------------------

QT       += core gui network xml

CONFIG += c++11
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = sysmo-operator
TEMPLATE = app


SOURCES += main.cpp\
    mainwindow.cpp \
    centralwidget.cpp \
    ngrid.cpp \
    ngridcontainer.cpp \
    nframe.cpp \
    nframecontainer.cpp \
    sidebutton.cpp \
    monitor/treeview.cpp \
    monitor/treemodel.cpp \
    monitor/itemtarget.cpp \
    monitor/delegateprobeprogress.cpp \
    monitor/itemprobe.cpp \
    monitor/menuprobe.cpp \
    monitor/menutarget.cpp \
    monitor/monitorwidget.cpp \
    monitor/monitor.cpp \
    dialogs/login.cpp \
    dialogs/newtarget.cpp \
    dialogs/newtargetpage1.cpp \
    network/supercast.cpp \
    network/supercastsocket.cpp \
    network/supercasthttp.cpp \
    network/supercastsignal.cpp \
    dialogs/newprobe.cpp \
    dialogs/newprobepage1.cpp \
    themes.cpp \
    dashboard/dashboardwidget.cpp \
    dashboard/dashboardtab.cpp \
    dialogs/messagebox.cpp \
    network/supercasthttprequest.cpp \
    network/supercasthttpreply.cpp \
    rrds/rrd4c.cpp \
    rrds/rrd4csocket.cpp \
    dialogs/newprobepage2.cpp \
    monitor/xml/nchecksimpleparser.cpp
    rrds/rrd4csignal.cpp

HEADERS  += mainwindow.h \
    centralwidget.h \
    ngrid.h \
    ngridcontainer.h \
    nframe.h \
    nframecontainer.h \
    sidebutton.h \
    monitor/treeview.h \
    monitor/treemodel.h \
    monitor/itemprobe.h \
    monitor/itemtarget.h \
    monitor/delegateprobeprogress.h \
    monitor/monitorwidget.h \
    monitor/monitor.h \
    monitor/menuprobe.h \
    monitor/menutarget.h \
    dialogs/login.h \
    dialogs/newtarget.h \
    dialogs/newtargetpage1.h \
    network/supercast.h \
    network/supercastsocket.h \
    network/supercasthttp.h \
    network/supercastsignal.h \
    dialogs/newprobe.h \
    dialogs/newprobepage1.h \
    themes.h \
    sysmo.h \
    dashboard/dashboardwidget.h \
    dashboard/dashboardtab.h \
    dialogs/messagebox.h \
    monitor/nchecks.h \
    network/supercasthttprequest.h \
    network/supercasthttpreply.h \
    rrds/rrd4c.h \
    rrds/rrd4csocket.h \
    rrds/rrd4csignal.h \
    dialogs/newprobepage2.h \
    monitor/xml/nchecksimpleparser.h

RESOURCES += \
    icons.qrc \
    box_icons.qrc \
    images.qrc \
    pixmaps.qrc \
    tree.qrc
