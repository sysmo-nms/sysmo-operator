from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
import  TkorderIcons

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class WorkView(QFrame):
    def __init__(self, parent):
        super(WorkView, self).__init__(parent)

        self.targetViews = dict()

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
        pass
        

    def createProbeView(self, probe):
        target = ChannelHandler.singleton.probes[probe]['target']
        if target not in self.targetViews.keys():
            targetView = WorkTargetView(self, target)
            self.mainGrid.addWidget(targetView, self.mainGrid.rowCount() + 1,0)
            self.targetViews[target] = targetView
        else:
            targetView = self.targetViews[target]
        targetView.addProbe(probe)

class WorkTargetView(QFrame):
    def __init__(self, parent, target):
        super(WorkTargetView, self).__init__(parent)
        self.head = QLabel(target, self)
        self.head.setFixedHeight(40)
        self.grid  = QGridLayout(self)
        self.grid.addWidget(self.head, 0,0)
        self.grid.setRowStretch(0,0)

    def addProbe(self, probe):
        print "passss"

class WorkProbeView(AbstractChannelQFrame):
    def __init__(self, parent, probe):
        super(WorkProbeView, self).__init__(parent, probe)
        self.probeName  = probe

    def handleProbeEvent(self, msg):
        print "workview probe event"

    def destroy(self):
        self.disconnectProbe(self.probeName)
        AbstractProbeView.destroy(self)
