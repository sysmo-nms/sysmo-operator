from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
from    LoggerViewEventsTimeLine    import EventsView
from    LoggerViewText              import TextLog
from    LoggerViewRrds              import *
from    WorkingProbeView            import ProbeView
from    WorkingTargetView           import TargetView

import  MonitorProxyEvents
import  TkorderIcons
import  os
import  datetime

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class WorkView(QFrame):
    def __init__(self, parent):
        super(WorkView, self).__init__(parent)

        self.tmpMainGridCount = 0

        self.targetViews = dict()

        self.mainGrid   = QGridLayout()
        self.mainFrame  = QFrame(self)
        #self.mainFrame.setBackgroundRole(QPalette.Dark)
        self.mainFrame.setLayout(self.mainGrid)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.mainFrame)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(Controls(self), 0,0)
        grid.addWidget(self.scroll, 1,0)
        self.setLayout(grid)

    def deleteProbeView(self, probe):
        t = MonitorProxyEvents.ChannelHandler.singleton.probes[probe]['target']
        r = self.targetViews[t].removeProbe(probe)
        if r == 'empty':
            self.mainGrid.removeWidget(self.targetViews[t])
            self.targetViews[t].deleteLater()
            self.mainGrid.update()
            del self.targetViews[t]

    def createProbeView(self, probe):
        # get the target from the probe
        t = MonitorProxyEvents.ChannelHandler.singleton.probes[probe]['target']
        # if not allready exist, create the target widget with probe as
        # argument
        if t in self.targetViews:
            self.targetViews[t].newProbe(probe)
        else:
            self.targetViews[t] = TargetView(self, t, probe)
            self.mainGrid.addWidget(self.targetViews[t], self.tmpMainGridCount, 0)
            self.tmpMainGridCount += 1
            self.mainGrid.setRowStretch(self.tmpMainGridCount, 0)
            self.mainGrid.setRowStretch(self.tmpMainGridCount + 1, 1)
            self.mainGrid.update()
