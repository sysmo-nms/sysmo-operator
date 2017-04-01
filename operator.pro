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

SOURCES += code/main.cpp /
    code/mainwindow.cpp /
    code/login.cpp /
    code/centralwidget.cpp /
    code/themes.cpp /
    code/logs/clog.c /
    code/widgets/lineedit.cpp /
    code/widgets/messagebox.cpp /
    code/widgets/nframecontainer.cpp /
    code/widgets/nframe.cpp /
    code/widgets/ngridcontainer.cpp /
    code/widgets/ngrid.cpp /
    code/widgets/nowheelcombobox.cpp /
    code/widgets/sidebutton.cpp /
    code/widgets/statusbutton.cpp /
    code/widgets/statusbuttonwidget.cpp /
    code/widgets/systemtray.cpp /
    code/widgets/temporarydir.cpp /
    code/applications/dashboard/dashboardtab.cpp /
    code/applications/dashboard/dashboardwidget.cpp /
    code/applications/dashboard/dialogs/newdashboard.cpp /
    code/applications/dashboard/dialogs/newdashboardp1.cpp /
    code/applications/logs/logswidget.cpp /
    code/applications/monitor/dialogs/newprobe.cpp /
    code/applications/monitor/dialogs/newprobepage1.cpp /
    code/applications/monitor/dialogs/newprobepage2.cpp /
    code/applications/monitor/dialogs/newprobepage3.cpp /
    code/applications/monitor/dialogs/newprobeprogressdialog.cpp /
    code/applications/monitor/dialogs/newtarget.cpp /
    code/applications/monitor/dialogs/newtargetpage1.cpp /
    code/applications/monitor/actions/actionprocess.cpp /
    code/applications/monitor/actions/monitoractionconfig.cpp /
    code/applications/monitor/actions/monitoractioncreate.cpp /
    code/applications/monitor/actions/monitoractions.cpp /
    code/applications/monitor/actions/monitoractionsdialog.cpp /
    code/applications/monitor/delegateprobeprogress.cpp /
    code/applications/monitor/itemprobe.cpp /
    code/applications/monitor/itemtarget.cpp /
    code/applications/monitor/menuprobe.cpp /
    code/applications/monitor/menutarget.cpp /
    code/applications/monitor/monitorchannel.cpp /
    code/applications/monitor/monitor.cpp /
    code/applications/monitor/monitorlogs.cpp /
    code/applications/monitor/monitorwidget.cpp /
    code/applications/monitor/nchecks.cpp /
    code/applications/monitor/treemodel.cpp /
    code/applications/monitor/treeview.cpp /
    code/applications/monitor/xml/parseallchecks.cpp /
    code/applications/monitor/xml/parsecheckgetid.cpp /
    code/applications/monitor/xml/parsecheckgetinfos.cpp /
    code/applications/monitor/xml/parsecheckmakedoc.cpp /
    code/applications/monitor/xml/parsecheckmakeform.cpp /
    code/applications/monitor/xml/parsecheckmakegraphcmd.cpp /
    code/applications/monitor/windows/probewindow.cpp /
    code/network/supercast.cpp /
    code/network/supercasthttp.cpp /
    code/network/supercasthttpreply.cpp /
    code/network/supercasthttprequest.cpp /
    code/network/supercastsignal.cpp /
    code/network/supercastsocket.cpp /
    code/network/qjson.cpp /
    code/network/socketutils.cpp /
    code/rrds/rrd4qt.cpp /
    code/rrds/rrd4qtgraph.cpp /
    code/rrds/rrd4qtproc.cpp /
    code/rrds/rrd4qtsignal.cpp

HEADERS  += code/sysmo.h /
    code/config.h /
    code/login.h /
    code/centralwidget.h /
    code/themes.h /
    code/logs/clog.h /
    code/widgets/lineedit.h /
    code/widgets/messagebox.h /
    code/widgets/nframecontainer.h /
    code/widgets/nframe.h /
    code/widgets/ngridcontainer.h /
    code/widgets/ngrid.h /
    code/widgets/nowheelcombobox.h /
    code/widgets/sidebutton.h /
    code/widgets/statusbutton.h /
    code/widgets/statusbuttonwidget.h /
    code/widgets/systemtray.h /
    code/widgets/temporarydir.h /
    code/applications/dashboard/dashboardtab.h /
    code/applications/dashboard/dashboardwidget.h /
    code/applications/dashboard/dialogs/newdashboard.h /
    code/applications/dashboard/dialogs/newdashboardp1.h /
    code/applications/logs/logswidget.h /
    code/applications/monitor/dialogs/newprobe.h /
    code/applications/monitor/dialogs/newprobepage1.h /
    code/applications/monitor/dialogs/newprobepage2.h /
    code/applications/monitor/dialogs/newprobepage3.h /
    code/applications/monitor/dialogs/newprobeprogressdialog.h /
    code/applications/monitor/dialogs/newtarget.h /
    code/applications/monitor/dialogs/newtargetpage1.h /
    code/applications/monitor/actions/actionprocess.h /
    code/applications/monitor/actions/monitoractionconfig.h /
    code/applications/monitor/actions/monitoractioncreate.h /
    code/applications/monitor/actions/monitoractionsdialog.h /
    code/applications/monitor/actions/monitoractions.h /
    code/applications/monitor/targetutils.h /
    code/applications/monitor/delegateprobeprogress.h /
    code/applications/monitor/itemprobe.h /
    code/applications/monitor/itemtarget.h /
    code/applications/monitor/menuprobe.h /
    code/applications/monitor/menutarget.h /
    code/applications/monitor/monitorchannel.h /
    code/applications/monitor/monitor.h /
    code/applications/monitor/monitorlogs.h /
    code/applications/monitor/monitorwidget.h /
    code/applications/monitor/nchecks.h /
    code/applications/monitor/treemodel.h /
    code/applications/monitor/treeview.h /
    code/applications/monitor/xml/parseallchecks.h /
    code/applications/monitor/xml/parsecheckgetid.h /
    code/applications/monitor/xml/parsecheckgetinfos.h /
    code/applications/monitor/xml/parsecheckmakedoc.h /
    code/applications/monitor/xml/parsecheckmakeform.h /
    code/applications/monitor/xml/parsecheckmakegraphcmd.h /
    code/applications/monitor/windows/probewindow.h /
    code/network/supercast.h /
    code/network/supercasthttp.h /
    code/network/supercasthttpreply.h /
    code/network/supercasthttprequest.h /
    code/network/supercastsignal.h /
    code/network/supercastsocket.h /
    code/network/qjson.h /
    code/network/socketutils.h /
    code/rrds/rrd4qtgraph.h /
    code/rrds/rrd4qt.h /
    code/rrds/rrd4qtproc.h /
    code/rrds/rrd4qtsignal.h

RESOURCES += ressources/icons.qrc \
    ressources/box_icons.qrc \
    ressources/images.qrc \
    ressources/pixmaps.qrc \
    ressources/tree.qrc \
    ressources/rrd4qt.qrc

target.path = /$(BINDIR)
INSTALLS += target
