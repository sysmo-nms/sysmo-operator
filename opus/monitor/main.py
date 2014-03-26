from    PySide.QtCore   import (
    QSettings,
    QTimeLine
)

from    opus.monitor                 import norrd
from    opus.monitor.trees_area.main import TreeContainer
from    opus.monitor.dash_area.main  import DashContainer
from    opus.monitor.proxy           import ChanHandler
from    noctopus_widgets             import NSplitterContainer

import  nocapi

class Central(NSplitterContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        Central.singleton = self
        nocapi.nConnectWillClose(self._willClose)
        self._initRrdtool()
        self._initChanProxy()

        self._initLayout()
        self._initDockWidget()
        self._initToggle()
        self._initViewMode()
        self._readSettings()

    def _initViewMode(self):
        nocapi.nConnectViewMode(self.setViewMode)
        self.setViewMode(nocapi.nGetViewMode())

    def _initToggle(self):
        self._collapseTimeline  = QTimeLine(100, self)
        self._collapseTimeline.setCurveShape(QTimeLine.EaseInOutCurve)
        self._collapseTimeline.setUpdateInterval(20)
        self._collapseTimeline.frameChanged[int].connect(self._setSplitterSize)
        nocapi.nConnectAppToggled(self.toggleButtonClicked)

    def _initDockWidget(self): pass
#         tko.addTopDockWidget(Summary(self), 'Monitori')

    def _initLayout(self):
#         self._rightDash  = MonitorDashboardArea.DashboardStack(self)
        self._leftTree  = TreeContainer(self)
        self._rightDash = DashContainer(self)
        self.addWidget(self._leftTree)
        self.addWidget(self._rightDash)

    def _initRrdtool(self):
        self._rrdtool = norrd.init(parent=self)

    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _readSettings(self):
        settings = QSettings("Noctopus NMS", "monitor")
        self.restoreGeometry(settings.value("monitor/geometry"))
        self.restoreState(settings.value("monitor/state"))
        oldPosition = settings.value("monitor/oldPosition")

        if oldPosition != None:
            self._oldPosition = oldPosition
        else:
            self._oldPosition = 300


    def _willClose(self):
        settings = QSettings("Noctopus NMS", "monitor")
        settings.setValue("monitor/geometry",   self.saveGeometry())
        settings.setValue("monitor/state",      self.saveState())
        settings.setValue("monitor/oldPosition", self._oldPosition)
        # close rrdtool thread (self._rrdtool.quit())

    # CALLS from noctopus_* modules
    def toggleButtonClicked(self, app):
        if app != 'monitor': return
        [left, _] = self.sizes()
        if left != 0:
            self._oldPosition = left
            self._collapseTimeline.setFrameRange(left, 0)
            self._collapseTimeline.start()
        else:
            self._collapseTimeline.setFrameRange(0, self._oldPosition)
            self._collapseTimeline.start()

    def _setSplitterSize(self, value):
        self.moveSplitter(value, 1)

    def setViewMode(self, mode):
        print "set viewwwwwwwww mode ", mode
