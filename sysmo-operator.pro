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
    monitor.cpp \
    dashboard.cpp \
    monitor_tree/treeview.cpp \
    monitor_tree/treemodel.cpp \
    monitor_tree/treedelegateprogress.cpp \
    dialogs/newtarget.cpp \
    dialogs/login.cpp \
    network/supercast.cpp \
    network/supercastsocket.cpp \
    network/supercasthttp.cpp \
    network/supercastsignal.cpp \
    network/supercastquery.cpp \
    monitor_tree/targetitem.cpp \
    monitor_tree/probeitem.cpp \
    monitor_tree/progressitem.cpp

HEADERS  += mainwindow.h \
    centralwidget.h \
    ngrid.h \
    ngridcontainer.h \
    nframe.h \
    nframecontainer.h \
    sidebutton.h \
    monitor.h \
    dashboard.h \
    monitor_tree/treeview.h \
    monitor_tree/treemodel.h \
    monitor_tree/treedelegateprogress.h \
    dialogs/newtarget.h \
    dialogs/login.h \
    network/supercast.h \
    network/supercastsocket.h \
    network/supercasthttp.h \
    network/supercastsignal.h \
    network/supercastquery.h \
    monitor_tree/targetitem.h \
    monitor_tree/probeitem.h \
    monitor_tree/progressitem.h

RESOURCES += \
    ressources.qrc
