from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    WorkingProbeView    import ProbeView


class TargetView(QFrame):
    def __init__(self, parent, target, probe):
        super(TargetView, self).__init__(parent)
        self.probeViews = dict()
        self.rowCount   = 1

        self.targetHead  = TargetHead(self, target)
        self.targetBody  = TargetBody(self)
        self.targetBodyGrid = QGridLayout(self)
        self.targetBody.setLayout(self.targetBodyGrid)

        tab         = QFrame(self)
        tab.setFixedWidth(10)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.targetHead, 0,0,1,2)
        self.grid.addWidget(tab,                      1,0)
        self.grid.addWidget(self.targetBody, 1,1)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.setLayout(self.grid)
        self.newProbe(probe)

    def toggleBody(self):
        if self.grid.itemAtPosition(1,1) == None:
            self.grid.addWidget(self.targetBody, 1, 1)
        else:
            self.grid.removeWidget(self.targetBody)

    def newProbe(self, probe):
        self.probeViews[probe] = ProbeView(self, probe)
        self.targetBodyGrid.addWidget(self.probeViews[probe], self.rowCount, 1)
        self.rowCount += 1

    def removeProbe(self, probe):
        self.targetBodyGrid.removeWidget(self.probeViews[probe])
        self.probeViews[probe].deleteLater()
        self.targetBodyGrid.update()
        del self.probeViews[probe]
        if len(self.probeViews) == 0:
            return 'empty'
        else:
            return 'full'

class TargetHead(QFrame):
    def __init__(self, parent, target):
        super(TargetHead, self).__init__(parent)
        #self.setBackgroundRole(QPalette.Window)
        #self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Sunken)

        self.toggleButton = QPushButton('Toggle', self)
        self.toggleButton.clicked.connect(parent.toggleBody)

        self.promoteCheck = QCheckBox('include in Dashboard', self)
        grid = QGridLayout(self)
        grid.addWidget(self.toggleButton,    0,0)
        grid.addWidget(QLabel(target, self), 0,1)
        grid.addWidget(self.promoteCheck,    0,3)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)
        grid.setColumnStretch(3,0)
        self.setLayout(grid)

class TargetBody(QFrame):
    def __init__(self, parent):
        super(TargetBody, self).__init__(parent)
