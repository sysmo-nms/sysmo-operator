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
        self._defineSlidePos()

    def _defineSlidePos(self):
        [left, right] = self.sizes()
        if left == 0:
            self._slidePos  = 'left'
        elif right == 0:
            self._slidePos  = 'right'
        else:
            self._slidePos  = 'center'

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
        oldPosition = int(settings.value("monitor/oldPosition"))

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
    def toggleButtonClicked(self, dictArg):
        app = dictArg['id']
        but = dictArg['button']
        
        self._defineSlidePos()
        if app != 'monitor': return

        print app, but, self._slidePos
        if   but == 'right' and self._slidePos == 'right':
            self._moveLeftFrom('right')
        elif but == 'left'  and self._slidePos == 'left':
            self._moveRightFrom('left')
        elif but == 'right' and self._slidePos == 'left':
            self._moveRightFrom('left')
        elif but == 'right' and self._slidePos == 'center':
            self._moveRightFrom('center')
        elif but == 'left'  and self._slidePos == 'right':
            self._moveLeftFrom('right')
        elif but == 'left'  and self._slidePos == 'center':
            self._moveLeftFrom('center')

    def _moveLeftFrom(self, fromStr):
        [left, right] = self.sizes()
        if fromStr == 'right':
            self._collapseTimeline.setFrameRange(left + right, self._oldPosition)
            self._collapseTimeline.start()
            self._slidePos = 'center'
        if fromStr == 'center':
            self._collapseTimeline.setFrameRange(self._oldPosition, 0)
            self._collapseTimeline.start()
            self._slidePos = 'left'

    def _moveRightFrom(self, fromStr):
        [left, right] = self.sizes()
        if fromStr == 'left':
            self._collapseTimeline.setFrameRange(0, self._oldPosition)
            self._collapseTimeline.start()
            self._slidePos = 'center'
        if fromStr == 'center':
            self._collapseTimeline.setFrameRange(self._oldPosition, left + right)
            self._collapseTimeline.start()
            self._slidePos = 'right'
        
    def _setSplitterSize(self, value):
        self.moveSplitter(value, 1)

    def setViewMode(self, mode): pass






