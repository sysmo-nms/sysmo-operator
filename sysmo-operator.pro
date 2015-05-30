#-------------------------------------------------
#
# Project created by QtCreator 2015-05-27T17:15:26
#
#-------------------------------------------------

QT       += core gui

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
    monitor_tree/treedelegateprogress.cpp

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
    monitor_tree/treedelegateprogress.h

RESOURCES += \
    ressources.qrc
