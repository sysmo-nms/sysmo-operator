#-------------------------------------------------
#
# Project created by QtCreator 2015-05-27T17:15:26
#
#-------------------------------------------------

QT       += core gui network xml

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

# log with line numbers and files
DEFINES += QT_MESSAGELOGCONTEXT

TARGET = sysmo-operator
TEMPLATE = app


SOURCES += src/main.cpp \
    src/mainwindow.cpp \
    src/centralwidget.cpp \
    src/ngrid.cpp \
    src/ngridcontainer.cpp \
    src/nframe.cpp \
    src/nframecontainer.cpp \
    src/sidebutton.cpp \
    src/monitor/treeview.cpp \
    src/monitor/treemodel.cpp \
    src/monitor/itemtarget.cpp \
    src/monitor/delegateprobeprogress.cpp \
    src/monitor/itemprobe.cpp \
    src/monitor/menuprobe.cpp \
    src/monitor/menutarget.cpp \
    src/monitor/monitorwidget.cpp \
    src/monitor/monitor.cpp \
    src/monitor/nchecks.cpp \
    src/dialogs/login.cpp \
    src/dialogs/newtarget.cpp \
    src/dialogs/newtargetpage1.cpp \
    src/network/supercast.cpp \
    src/network/supercastsocket.cpp \
    src/network/supercasthttp.cpp \
    src/network/supercastsignal.cpp \
    src/dialogs/newprobe.cpp \
    src/dialogs/newprobepage1.cpp \
    src/themes.cpp \
    src/dashboard/dashboardwidget.cpp \
    src/dashboard/dashboardtab.cpp \
    src/dialogs/messagebox.cpp \
    src/network/supercasthttprequest.cpp \
    src/network/supercasthttpreply.cpp \
    src/dialogs/newprobepage2.cpp \
    src/monitor/xml/parseallchecks.cpp \
    src/monitor/xml/parsecheckgetid.cpp \
    src/monitor/xml/parsecheckgetinfos.cpp \
    src/monitor/xml/parsecheckmakedoc.cpp \
    src/monitor/xml/parsecheckmakeform.cpp \
    src/dialogs/newprobepage3.cpp \
    src/dialogs/newprobeprogressdialog.cpp \
    src/windows/probewindow.cpp \
    src/monitor/monitorchannel.cpp \
    src/monitor/xml/parsecheckmakegraphcmd.cpp \
    src/rrds/rrd4qtsignal.cpp \
    src/rrds/rrd4qtgraph.cpp \
    src/rrds/rrd4qt.cpp \
    src/actions/monitoractions.cpp \
    src/actions/monitoractionsdialog.cpp \
    src/actions/monitoractioncreate.cpp \
    src/actions/actionprocess.cpp \
    src/systemtray.cpp \
    src/nowheelcombobox.cpp \
    src/monitor/monitorlogs.cpp \
    src/actions/monitoractionconfig.cpp \
    src/statusbutton.cpp \
    src/statusbuttonwidget.cpp \
    src/qjson.cpp \
    src/temporarydir.cpp \
    src/rrds/rrd4qtproc.cpp

HEADERS  += include/mainwindow.h \
    include/centralwidget.h \
    include/ngrid.h \
    include/ngridcontainer.h \
    include/nframe.h \
    include/nframecontainer.h \
    include/sidebutton.h \
    include/monitor/treeview.h \
    include/monitor/treemodel.h \
    include/monitor/itemprobe.h \
    include/monitor/itemtarget.h \
    include/monitor/delegateprobeprogress.h \
    include/monitor/monitorwidget.h \
    include/monitor/monitor.h \
    include/monitor/menuprobe.h \
    include/monitor/menutarget.h \
    include/monitor/nchecks.h \
    include/dialogs/login.h \
    include/dialogs/newtarget.h \
    include/dialogs/newtargetpage1.h \
    include/network/supercast.h \
    include/network/supercastsocket.h \
    include/network/supercasthttp.h \
    include/network/supercastsignal.h \
    include/dialogs/newprobe.h \
    include/dialogs/newprobepage1.h \
    include/themes.h \
    include/sysmo.h \
    include/dashboard/dashboardwidget.h \
    include/dashboard/dashboardtab.h \
    include/dialogs/messagebox.h \
    include/network/supercasthttprequest.h \
    include/network/supercasthttpreply.h \
    include/dialogs/newprobepage2.h \
    include/monitor/xml/parseallchecks.h \
    include/monitor/xml/parsecheckgetid.h \
    include/monitor/xml/parsecheckgetinfos.h \
    include/monitor/xml/parsecheckmakedoc.h \
    include/monitor/xml/parsecheckmakeform.h \
    include/dialogs/newprobepage3.h \
    include/dialogs/newprobeprogressdialog.h \
    include/windows/probewindow.h \
    include/monitor/monitorchannel.h \
    include/monitor/xml/parsecheckmakegraphcmd.h \
    include/rrds/rrd4qtsignal.h \
    include/rrds/rrd4qtgraph.h \
    include/rrds/rrd4qt.h \
    include/actions/monitoractions.h \
    include/actions/monitoractionsdialog.h \
    include/actions/monitoractioncreate.h \
    include/actions/actionprocess.h \
    include/systemtray.h \
    include/nowheelcombobox.h \
    include/monitor/monitorlogs.h \
    include/actions/monitoractionconfig.h \
    include/statusbutton.h \
    include/statusbuttonwidget.h \
    include/qjson.h \
    include/temporarydir.h \
    include/rrds/rrd4qtproc.h

RESOURCES += ressources/icons.qrc \
    ressources/box_icons.qrc \
    ressources/images.qrc \
    ressources/pixmaps.qrc \
    ressources/tree.qrc \
    ressources/rrd4qt.qrc

target.path = /$(BINDIR)
INSTALLS += target
