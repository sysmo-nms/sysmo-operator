#-------------------------------------------------
#
# Project created by QtCreator 2015-05-27T17:15:26
#
#-------------------------------------------------

QT       += core gui network xml

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

# QWebSocket only available in 5.3
greaterThan(QT_VERSION, 5.2): {
    QT += websockets
    DEFINES += USE_WEBSOCKET
}

# add include
INCLUDEPATH += code/

# log with line numbers and files
DEFINES += QT_MESSAGELOGCONTEXT

TARGET = sysmo-operator
TEMPLATE = app

SOURCES += code/main.cpp \
    code/mainwindow.cpp \
    code/centralwidget.cpp \
    code/ngrid.cpp \
    code/ngridcontainer.cpp \
    code/nframe.cpp \
    code/nframecontainer.cpp \
    code/sidebutton.cpp \
    code/monitor/treeview.cpp \
    code/monitor/treemodel.cpp \
    code/monitor/itemtarget.cpp \
    code/monitor/delegateprobeprogress.cpp \
    code/monitor/itemprobe.cpp \
    code/monitor/menuprobe.cpp \
    code/monitor/menutarget.cpp \
    code/monitor/monitorwidget.cpp \
    code/monitor/monitor.cpp \
    code/monitor/nchecks.cpp \
    code/dialogs/login.cpp \
    code/dialogs/newtarget.cpp \
    code/dialogs/newtargetpage1.cpp \
    code/network/supercast.cpp \
    code/network/supercasthttp.cpp \
    code/network/supercastsignal.cpp \
    code/dialogs/newprobe.cpp \
    code/dialogs/newprobepage1.cpp \
    code/themes.cpp \
    code/dashboard/dashboardwidget.cpp \
    code/dashboard/dashboardtab.cpp \
    code/dialogs/messagebox.cpp \
    code/network/supercasthttprequest.cpp \
    code/network/supercasthttpreply.cpp \
    code/dialogs/newprobepage2.cpp \
    code/monitor/xml/parseallchecks.cpp \
    code/monitor/xml/parsecheckgetid.cpp \
    code/monitor/xml/parsecheckgetinfos.cpp \
    code/monitor/xml/parsecheckmakedoc.cpp \
    code/monitor/xml/parsecheckmakeform.cpp \
    code/dialogs/newprobepage3.cpp \
    code/dialogs/newprobeprogressdialog.cpp \
    code/windows/probewindow.cpp \
    code/monitor/monitorchannel.cpp \
    code/monitor/xml/parsecheckmakegraphcmd.cpp \
    code/rrds/rrd4qtsignal.cpp \
    code/rrds/rrd4qtgraph.cpp \
    code/rrds/rrd4qt.cpp \
    code/actions/monitoractions.cpp \
    code/actions/monitoractionsdialog.cpp \
    code/actions/monitoractioncreate.cpp \
    code/actions/actionprocess.cpp \
    code/actions/monitoractionconfig.cpp \
    code/systemtray.cpp \
    code/nowheelcombobox.cpp \
    code/monitor/monitorlogs.cpp \
    code/statusbutton.cpp \
    code/statusbuttonwidget.cpp \
    code/qjson.cpp \
    code/temporarydir.cpp \
    code/rrds/rrd4qtproc.cpp \
    code/rotatingfilelogger.cpp \
    code/lineedit.cpp

HEADERS  += code/mainwindow.h \
    code/centralwidget.h \
    code/ngrid.h \
    code/ngridcontainer.h \
    code/nframe.h \
    code/nframecontainer.h \
    code/sidebutton.h \
    code/monitor/treeview.h \
    code/monitor/treemodel.h \
    code/monitor/itemprobe.h \
    code/monitor/itemtarget.h \
    code/monitor/delegateprobeprogress.h \
    code/monitor/monitorwidget.h \
    code/monitor/monitor.h \
    code/monitor/menuprobe.h \
    code/monitor/menutarget.h \
    code/monitor/nchecks.h \
    code/dialogs/login.h \
    code/dialogs/newtarget.h \
    code/dialogs/newtargetpage1.h \
    code/network/supercast.h \
    code/network/supercasthttp.h \
    code/network/supercastsignal.h \
    code/dialogs/newprobe.h \
    code/dialogs/newprobepage1.h \
    code/themes.h \
    code/sysmo.h \
    code/dashboard/dashboardwidget.h \
    code/dashboard/dashboardtab.h \
    code/dialogs/messagebox.h \
    code/network/supercasthttprequest.h \
    code/network/supercasthttpreply.h \
    code/dialogs/newprobepage2.h \
    code/monitor/xml/parseallchecks.h \
    code/monitor/xml/parsecheckgetid.h \
    code/monitor/xml/parsecheckgetinfos.h \
    code/monitor/xml/parsecheckmakedoc.h \
    code/monitor/xml/parsecheckmakeform.h \
    code/dialogs/newprobepage3.h \
    code/dialogs/newprobeprogressdialog.h \
    code/windows/probewindow.h \
    code/monitor/monitorchannel.h \
    code/monitor/xml/parsecheckmakegraphcmd.h \
    code/rrds/rrd4qtsignal.h \
    code/rrds/rrd4qtgraph.h \
    code/rrds/rrd4qt.h \
    code/actions/monitoractions.h \
    code/actions/monitoractionsdialog.h \
    code/actions/monitoractioncreate.h \
    code/actions/actionprocess.h \
    code/actions/monitoractionconfig.h \
    code/systemtray.h \
    code/nowheelcombobox.h \
    code/monitor/monitorlogs.h \
    code/statusbutton.h \
    code/statusbuttonwidget.h \
    code/qjson.h \
    code/temporarydir.h \
    code/rrds/rrd4qtproc.h \
    code/rotatingfilelogger.h \
    code/lineedit.h


contains(DEFINES, USE_WEBSOCKET): {
  SOURCES += code/network/supercastwebsocket.cpp
  HEADERS += code/network/supercastwebsocket.h
} else {
  SOURCES += code/network/supercastsocket.cpp
  HEADERS += code/network/supercastsocket.h
}

RESOURCES += ressources/icons.qrc \
    ressources/box_icons.qrc \
    ressources/images.qrc \
    ressources/pixmaps.qrc \
    ressources/tree.qrc \
    ressources/rrd4qt.qrc \
    ressources/cssressource.qrc

target.path = /$(BINDIR)
INSTALLS += target
