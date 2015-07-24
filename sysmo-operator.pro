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
    monitor/nchecks.cpp \
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
    dialogs/newprobepage2.cpp \
    monitor/xml/parseallchecks.cpp \
    monitor/xml/parsecheckgetid.cpp \
    monitor/xml/parsecheckgetinfos.cpp \
    monitor/xml/parsecheckmakedoc.cpp \
    monitor/xml/parsecheckmakeform.cpp \
    dialogs/newprobepage3.cpp \
    dialogs/newprobeprogressdialog.cpp \
    windows/probewindow.cpp \
    monitor/monitorchannel.cpp \
    monitor/xml/parsecheckmakegraphcmd.cpp \
    rrds/rrd4qtsignal.cpp \
    rrds/rrd4qtgraph.cpp \
    rrds/rrd4qt.cpp

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
    monitor/nchecks.h \
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
    network/supercasthttprequest.h \
    network/supercasthttpreply.h \
    dialogs/newprobepage2.h \
    monitor/xml/parseallchecks.h \
    monitor/xml/parsecheckgetid.h \
    monitor/xml/parsecheckgetinfos.h \
    monitor/xml/parsecheckmakedoc.h \
    monitor/xml/parsecheckmakeform.h \
    dialogs/newprobepage3.h \
    dialogs/newprobeprogressdialog.h \
    windows/probewindow.h \
    monitor/monitorchannel.h \
    monitor/xml/parsecheckmakegraphcmd.h \
    rrds/rrd4qtsignal.h \
    rrds/rrd4qtgraph.h \
    rrds/rrd4qt.h

RESOURCES += \
    icons.qrc \
    box_icons.qrc \
    images.qrc \
    pixmaps.qrc \
    tree.qrc \
    rrd4qt.qrc
