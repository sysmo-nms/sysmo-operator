from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    TargetProbeView import ProbeView
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile


class TargetView(QFrame):
    probeDumpSignal     = Signal(dict)
    probeReturnSignal   = Signal(dict)

    def __init__(self, parent, targetName):
        super(TargetView, self).__init__(parent)
        self.head   = TargetViewHead(self, targetName)
        self.scroll = TargetViewScroll(self, targetName)
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.head, 0, 0)
        grid.addWidget(self.scroll, 1, 0)
        self.setLayout(grid)

    def handleProbeReturn(self, msg):
        self.probeReturnSignal.emit(msg)
        self.scroll.handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        self.probeReturnSignal.emit(msg)
        self.scroll.handleProbeDump(msg)

class TargetViewHead(QFrame):
    def __init__(self, parent, targetName):
        super(TargetViewHead, self).__init__(parent)
        self.headLabel = QLabel(targetName)
        self.headLabel.setFrameStyle(1),
        self.headLabel.setFrameShadow(QFrame.Raised)
        grid = QGridLayout()
        grid.addWidget(self.headLabel, 0, 0)
        self.setLayout(grid)

class TargetViewScroll(QScrollArea):
    def __init__(self, parent, targetName):
        super(TargetViewScroll, self).__init__(parent)
        self.content = TargetViewBody(self, targetName)
        self.setWidget(self.content)
        self.setWidgetResizable(True)

    def handleProbeReturn(self, msg):
        self.content.handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        self.content.handleProbeDump(msg)

class TargetViewBody(QFrame):

    def __init__(self, parent, targetName):
        super(TargetViewBody, self).__init__(parent)
        targetDict = ModTracker.TrackerMain.singleton.targets[targetName]
        self.grid = QGridLayout()
        for probeId in targetDict:
            self.grid.addWidget(ProbeView(self, 
                targetName, probeId, targetDict[probeId]), probeId, 0)
        self.setLayout(self.grid)

    def handleProbeReturn(self, msg):
        probeId     = msg['value']['id']
        probeLayout = self.grid.itemAtPosition(probeId, 0)
        probeView   = probeLayout.widget()
        probeView.handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        probeId     = msg['value']['id']
        probeLayout = self.grid.itemAtPosition(probeId, 0)
        probeView   = probeLayout.widget()
        probeView.handleProbeDump(msg)
