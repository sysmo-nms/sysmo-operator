from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    WorkingProbeView    import ProbeView


class TargetView(QFrame):
    def __init__(self, parent, target, probe):
        super(TargetView, self).__init__(parent)
        self.probeViews = dict()
        self.rowCount   = 1
        tab = QFrame(self)
        tab.setFixedWidth(10)

        self.grid = QGridLayout(self)
        self.grid.addWidget(TargetHead(self, target), 0,0,1,2)
        self.grid.addWidget(tab,                      1,0)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.setLayout(self.grid)
        self.newProbe(probe)

    def newProbe(self, probe):
        self.probeViews[probe] = ProbeView(self, probe)
        self.grid.addWidget(self.probeViews[probe], self.rowCount, 1)
        self.rowCount += 1

    def removeProbe(self, probe):
        self.grid.removeWidget(self.probeViews[probe])
        self.probeViews[probe].deleteLater()
        self.grid.update()
        del self.probeViews[probe]
        if len(self.probeViews) == 0:
            return 'empty'
        else:
            return 'full'

class TargetHead(QFrame):
    def __init__(self, parent, target):
        super(TargetHead, self).__init__(parent)
        self.setBackgroundRole(QPalette.Window)
        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.StyledPanel)
        grid = QGridLayout(self)
        grid.addWidget(QLabel(target, self), 0,0)
        self.setLayout(grid)
