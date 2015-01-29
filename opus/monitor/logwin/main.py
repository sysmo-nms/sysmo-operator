from    PyQt4.QtCore   import (
    QSettings,
    QSize,
    QTimeLine,
    pyqtSignal,
    Qt
)

from    PyQt4.QtGui    import (
    QWidget,
    QDialog,
    QScrollArea,
    QPixmap,
    QPalette,
    QFont,
    QStatusBar,
    QProgressBar,
    QPushButton,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QTabWidget
)

from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid,
    QLabel
)

from    opus.monitor.proxy           import AbstractChannelWidget, ChanHandler
from    opus.monitor.logwin.rrdarea  import RrdArea
import  opus.monitor.api    as monapi
import  opus.monitor.norrd  as norrd

import  nocapi
import  platform
import  re

# TODO
# - graphs in a QTreeView (filtre, classer par interface speed)
# - ajouter "next return"
# - ajouter QTimeLine: move/redraw
# - ajouter indicateur "redrawing"


def openLoggerFor(probe, displayName):
    if probe in list(LoggerView.Elements.keys()):
        LoggerView.Elements[probe].show()
        return
    else:
        LoggerView.Elements[probe] = LoggerView(probe, displayName)

class LoggerView(QDialog):
    Elements = dict()
    def __init__(self, probe, displayName, parent=None):
        super(LoggerView, self).__init__(parent)

        self._statusBar = LogStatusBar(self)
        self._menus     = ProbeMenus(self)

        loggers = list(ChanHandler.singleton.probes[probe]['loggers'].keys())
        rrdlogger   = False
        textlogger  = False
        eventlogger = False
        if 'bmonitor_logger_rrd2'    in loggers: rrdlogger = True
        if 'bmonitor_logger_text'   in loggers: textlogger = True
        if 'bmonitor_logger_event'  in loggers: eventlogger = True

        self._logArea   = LogArea(self, rrdlogger, textlogger, eventlogger, probe)

        self._layout    = NGrid(self)
        self._layout.addWidget(self._menus,     0,0)
        self._layout.addWidget(self._logArea,   0,1)
        self._layout.addWidget(self._statusBar, 1,0,1,2)

        self._layout.setRowStretch(0,1)
        self._layout.setRowStretch(1,0)

        self._layout.setColumnStretch(0,0)
        self._layout.setColumnStretch(1,1)


        self.show()
 
class LogArea(NFrameContainer):
    def __init__(self, parent, rrd, text, event, probe):
        super(LogArea, self).__init__(parent)
        self._layout = NGridContainer(self)

        self._tabs   = QTabWidget(self)
        self._layout.addWidget(self._tabs, 0,0)

        if event == True:
            self._events = QLabel('events', self)
            self._layout.addWidget(self._events, 1,0)
            self._layout.setRowStretch(1,0)
        else:
            self._events = None

        if rrd == True:
            self._rrds = RrdArea(self, probe)
            self._tabs.insertTab(0, self._rrds, nocapi.nGetPixmap('rrdtool-logo'), 'RRD')
        else:
            self._rrds = QLabel('rrds', self)
            self._tabs.insertTab(0, self._rrds, nocapi.nGetPixmap('rrdtool-logo'), 'RRD')
            self._tabs.setTabEnabled(0, False)

        if text == True:
            self._rrds = QLabel('text', self)
            self._tabs.insertTab(1, self._rrds, nocapi.nGetIcon('accessories-text-editor'), 'Text')
            if self._tabs.isTabEnabled(0) == False:
                self._tabs.setCurrentIndex(1)
        else:
            self._rrds = QLabel('text', self)
            self._tabs.insertTab(1, self._rrds, nocapi.nGetIcon('accessories-text-editor'), 'Text')
            self._tabs.setTabEnabled(1, False)


class LogStatusBar(QStatusBar):
    def __init__(self, parent):
        super(LogStatusBar, self).__init__(parent)
 

class ProbeMenus(NFrameContainer):
    def __init__(self, parent):
        super(ProbeMenus, self).__init__(parent)
        self._force = QPushButton(self)
        self._force.setIconSize(QSize(30,30))
        self._force.setIcon(nocapi.nGetIcon('software-update-available'))
        self._pause = QPushButton(self)
        self._pause.setIconSize(QSize(30,30))
        self._pause.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self._pause.setCheckable(True)
        self._pause.setChecked(False)
        self._action = QPushButton(self)
        self._action.setIconSize(QSize(30,30))
        self._action.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self._prop = QPushButton(self)
        self._prop.setIconSize(QSize(30,30))
        self._prop.setIcon(nocapi.nGetIcon('edit-paste'))

        grid = NGridContainer(self)
        grid.setVerticalSpacing(4)
        grid.addWidget(self._force,  0,1)
        grid.addWidget(self._pause,  1,1)
        grid.addWidget(self._action, 2,1)
        grid.addWidget(self._prop,   4,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,0)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,0)
        self.setLayout(grid)



# class LoggerView2(QDialog):
#     Elements = dict()
#     def __init__(self, probe, displayName, parent=None):
#         super(LoggerView2, self).__init__(parent)
#         nocapi.nConnectWillClose(self._willClose)
#         self._element = probe
#         self.setWindowTitle(displayName)
# 
#         self._statusBar = LogStatusBar(self)
# 
#         menus       = ProbeMenus(self)
# 
#         scrollArea  = RrdArea(self, probe)
# 
#         grid = NGrid(self)
#         grid.addWidget(scrollArea, 0,1)
#         grid.addWidget(menus,      0,0)
#         grid.addWidget(self._statusBar,  1,0,1,2)
#         grid.setRowStretch(0,1)
#         grid.setRowStretch(1,0)
# 
#         self.setLayout(grid)
#         self.show()
# 
#     def setProgressMax(self, maxi):
#         self._statusBar.progress.setMaximum(maxi)
# 
#     def updateProgress(self, fileId):
#         self._statusBar.updateProgress(fileId)
# 
#     def _restoreSettings(self):
#         settings = QSettings()
#         settingsString = 'monitor/element_perf_geometry/%s' % self._element
#         geometry = settings.value(settingsString)
#         if geometry != None:
#             self.restoreGeometry(geometry)
# 
#     def _saveSettings(self):
#         settings = QSettings()
#         settingsString = 'monitor/element_perf_geometry/%s' % self._element
#         settings.setValue(settingsString, self.saveGeometry())
# 
#     def _willClose(self):
#         self._saveSettings()
#         self.close()
# 
#     def show(self):
#         self._restoreSettings()
#         self.raise_()
#         QDialog.show(self)
# 
#     def closeEvent(self, event):
#         self._saveSettings()
#         QDialog.closeEvent(self, event)
# 
# class ProbeMenus(NFrameContainer):
#     def __init__(self, parent):
#         super(ProbeMenus, self).__init__(parent)
#         self._force = QPushButton(self)
#         self._force.setIconSize(QSize(30,30))
#         self._force.setIcon(nocapi.nGetIcon('software-update-available'))
#         self._pause = QPushButton(self)
#         self._pause.setIconSize(QSize(30,30))
#         self._pause.setIcon(nocapi.nGetIcon('media-playback-pause'))
#         self._pause.setCheckable(True)
#         self._pause.setChecked(False)
#         self._action = QPushButton(self)
#         self._action.setIconSize(QSize(30,30))
#         self._action.setIcon(nocapi.nGetIcon('utilities-terminal'))
#         self._prop = QPushButton(self)
#         self._prop.setIconSize(QSize(30,30))
#         self._prop.setIcon(nocapi.nGetIcon('edit-paste'))
# 
#         grid = NGridContainer(self)
#         grid.setVerticalSpacing(4)
#         grid.addWidget(self._force,  0,1)
#         grid.addWidget(self._pause,  1,1)
#         grid.addWidget(self._action, 2,1)
#         grid.addWidget(self._prop,   4,1)
#         grid.setRowStretch(0,0)
#         grid.setRowStretch(1,0)
#         grid.setRowStretch(2,0)
#         grid.setRowStretch(3,1)
#         grid.setRowStretch(4,0)
#         self.setLayout(grid)
# 
# 
# class LogStatusBar(QStatusBar):
#     def __init__(self, parent):
#         super(LogStatusBar, self).__init__(parent)
#         self.progress = QProgressBar(self)
#         self.progress.setMinimum(0)
#         self.progress.setValue(0)
#         self.addPermanentWidget(self.progress)
# 
#     def updateProgress(self, info):
#         val = self.progress.value()
#         self.progress.setValue(val + 1)
#         self.progress.setFormat('Loading data: %p%')
#         self.showMessage('Loading RRD file for If %s' % info)
#         if self.progress.maximum() == val + 1:
#             self.removeWidget(self.progress)
#             self.showMessage('Load complete', timeout=2000)
# 
# 
# class RrdArea(NFrameContainer):
#     def __init__(self, parent, probe):
#         super(RrdArea, self).__init__(parent)
#         self._rrdFrame = RrdLog2(self, probe, parent)
#         rrdScroll = QScrollArea(self)
#         rrdScroll.setWidget(self._rrdFrame)
#         rrdScroll.setWidgetResizable(True)
# 
#         rrdControls = RrdControls(self)
#         grid = NGridContainer(self)
#         grid.setVerticalSpacing(4)
#         grid.addWidget(rrdControls,          0,0)
#         grid.addWidget(rrdScroll,            1,0)
#         self.setLayout(grid)
# 
#     def timelineMove(self, start, end):
#         self._rrdFrame.setTimeline(start, end)
# 
#     def heightMove(self, size):
#         self._rrdFrame.setGraphHeight(size)
# 
# class RrdControls(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdControls, self).__init__(parent)
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(20)
#         grid.setContentsMargins(20,0,20,0)
#         lo   = RrdLocateControl(self)
#         tl   = RrdTimelineControl(self, parent)
#         rh   = RrdHeightControl(self, parent)
#         un   = RrdUnifyControl(self)
#         la   = RrdLayoutControl(self)
# 
#         #
#         lo.setDisabled(True)
#         un.setDisabled(True)
#         la.setDisabled(True)
#         #
#         grid.addWidget(lo,          0,0)
#         grid.addWidget(tl,          0,1)
#         grid.addWidget(rh,          0,2)
#         grid.addWidget(un,          0,3)
#         grid.addWidget(la,          0,4)
#         grid.setColumnStretch(0,0)
#         grid.setColumnStretch(1,0)
#         grid.setColumnStretch(2,0)
#         grid.setColumnStretch(3,0)
#         grid.setColumnStretch(4,0)
#         grid.setColumnStretch(5,1)
#         self.setLayout(grid)
# 
# 
# class RrdLayoutControl(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdLayoutControl, self).__init__(parent)
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         heightLab = QLabel('Layout:', self)
#         height = QComboBox(self)
#         height.addItem('1 column')
#         height.addItem('2 columns')
#         height.addItem('3 columns')
#         height.addItem('4 columns')
#         grid.addWidget(heightLab,   0,0)
#         grid.addWidget(height,      0,1)
#         self.setLayout(grid)
# 
# class RrdLocateControl(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdLocateControl, self).__init__(parent)
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         locateOr = QComboBox(self)
#         locateOr.addItem('Locate:')
#         locateOr.addItem('Filter:')
#         line = QLineEdit(self)
#         line.setMinimumWidth(150)
#         grid.addWidget(locateOr, 0,0)
#         grid.addWidget(line,     0,1)
#         self.setLayout(grid)
# 
# class RrdUnifyControl(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdUnifyControl, self).__init__(parent)
#         grid = NGridContainer(self)
#         unify = QCheckBox('Unify Y axis', self)
#         grid.addWidget(unify, 0,0)
#         self.setLayout(grid)
# 
# class RrdHeightControl(NFrameContainer):
#     def __init__(self, parent, master):
#         super(RrdHeightControl, self).__init__(parent)
#         self._master = master
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         heightLab = QLabel('Graph height:', self)
#         height = QComboBox(self)
#         height.insertItem(0, 'Thumbnail')
#         height.insertItem(1, 'Small')
#         height.insertItem(2, 'Normal')
#         height.insertItem(3, 'Large')
#         height.insertItem(4, 'Huge')
#         height.currentIndexChanged[int].connect(self._heightMove)
#         grid.addWidget(heightLab,   0,0)
#         grid.addWidget(height,      0,1)
#         self.setLayout(grid)
# 
#     def _heightMove(self, index):
#         if index == 0:
#             self._master.heightMove(31)
#         elif index == 1:
#             self._master.heightMove(80)
#         elif index == 2:
#             self._master.heightMove(100)
#         elif index == 3:
#             self._master.heightMove(130)
#         elif index == 4:
#             self._master.heightMove(180)
# 
# 
# 
# class RrdTimelineControl(NFrameContainer):
#     def __init__(self, parent, master):
#         super(RrdTimelineControl, self).__init__(parent)
#         self._master = master
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         timeLineLab = QLabel('Timeline:', self)
#         timeLine = QComboBox(self)
#         timeLine.insertItem(0, '2h  from now')
#         timeLine.insertItem(1, '12h from now')
#         timeLine.insertItem(2, '2d  from now')
#         timeLine.insertItem(3, '7d  from now')
#         timeLine.insertItem(4, '2w  from now')
#         timeLine.insertItem(5, '1m  from now')
#         timeLine.insertItem(6, '6m  from now')
#         timeLine.insertItem(7, '1y  from now')
#         timeLine.insertItem(8, '3y  from now')
#         timeLine.insertItem(9, '10y from now')
#         timeLine.currentIndexChanged[int].connect(self._timelineMove)
#         grid.addWidget(timeLineLab, 0,0)
#         grid.addWidget(timeLine,    0,1)
#         self.setLayout(grid)
# 
#     def _timelineMove(self, index):
#         if index == 0:
#             start   = 'now-2hours'
#             end     = 'now'
#             self._master.timelineMove(start, end)
#         if index == 1:
#             start   = 'now-12hours'
#             end     = 'now'
#             self._master.timelineMove(start, end)
#         elif index == 2:
#             end     = 'now'
#             start   = 'now-2days'
#             self._master.timelineMove(start, end)
#         elif index == 3:
#             end     = 'now'
#             start   = 'now-7days'
#             self._master.timelineMove(start, end)
#         elif index == 4:
#             end     = 'now'
#             start   = 'now-2weeks'
#             self._master.timelineMove(start, end)
#         elif index == 5:
#             end     = 'now'
#             start   = 'now-1month'
#             self._master.timelineMove(start, end)
#         elif index == 6:
#             end     = 'now'
#             start   = 'now-6months'
#             self._master.timelineMove(start, end)
#         elif index == 7:
#             end     = 'now'
#             start   = 'now-1year'
#             self._master.timelineMove(start, end)
#         elif index == 8:
#             end     = 'now'
#             start   = 'now-3years'
#             self._master.timelineMove(start, end)
#         elif index == 9:
#             end     = 'now'
#             start   = 'now-10years'
#             self._master.timelineMove(start, end)
