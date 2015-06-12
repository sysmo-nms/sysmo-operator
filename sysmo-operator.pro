#-------------------------------------------------
#
# Project created by QtCreator 2015-05-27T17:15:26
#
#-------------------------------------------------

QT       += core gui network

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
    dashboard.cpp \
    monitor_tree/treeview.cpp \
    monitor_tree/treemodel.cpp \
    monitor_tree/itemtarget.cpp \
    monitor_tree/delegateprobeprogress.cpp \
    monitor_tree/itemprobe.cpp \
    dialogs/login.cpp \
    dialogs/newtarget.cpp \
    dialogs/newtargetpage1.cpp \
    network/supercast.cpp \
    network/supercastsocket.cpp \
    network/supercasthttp.cpp \
    network/supercastsignal.cpp \
    network/supercastquery.cpp \
    themes.cpp \
    monitor_tree/menuprobe.cpp \
    monitor_tree/menutarget.cpp \
    dialogs/newprobe.cpp \
    dialogs/newprobepage1.cpp \
    monitorwidget.cpp \
    monitor.cpp

HEADERS  += mainwindow.h \
    centralwidget.h \
    ngrid.h \
    ngridcontainer.h \
    nframe.h \
    nframecontainer.h \
    sidebutton.h \
    dashboard.h \
    monitor_tree/treeview.h \
    monitor_tree/treemodel.h \
    monitor_tree/itemprobe.h \
    monitor_tree/itemtarget.h \
    monitor_tree/delegateprobeprogress.h \
    dialogs/login.h \
    dialogs/newtarget.h \
    dialogs/newtargetpage1.h \
    network/supercast.h \
    network/supercastsocket.h \
    network/supercasthttp.h \
    network/supercastsignal.h \
    network/supercastquery.h \
    themes.h \
    sysmo.h \
    monitor_tree/menuprobe.h \
    monitor_tree/menutarget.h \
    dialogs/newprobe.h \
    dialogs/newprobepage1.h \
    monitorwidget.h \
    monitor.h

RESOURCES += \
    icons.qrc \
    images.qrc \
    pixmaps.qrc \
    tree.qrc
