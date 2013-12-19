from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
from    LoggerViewEventsTimeLine    import EventsView
from    LoggerViewText              import TextLog
from    LoggerViewRrds              import *
from    WorkingProbeView            import ProbeView

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

        self.probeViews = dict()

        self.mainGrid   = QGridLayout()
        self.mainFrame  = QFrame(self)
        self.mainFrame.setBackgroundRole(QPalette.Base)
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
        probeView = self.probeViews[probe]
        self.mainGrid.removeWidget(probeView)
        probeView.deleteLater()
        self.mainGrid.update()
        
        del self.probeViews[probe]

    def createProbeView(self, probe):
        pview = ProbeView(self, probe)
        self.probeViews[probe] = pview
        self.mainGrid.addWidget(pview, self.tmpMainGridCount, 0)
        self.tmpMainGridCount += 1
        self.mainGrid.setRowStretch(self.tmpMainGridCount, 0)
        self.mainGrid.setRowStretch(self.tmpMainGridCount + 1, 1)
        self.mainGrid.update()
