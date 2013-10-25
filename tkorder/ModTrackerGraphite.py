from    PySide.QtGui     import *

class ElementView(QScrollArea):
    def __init__(self, parent, targetName, probeId, targetDict):
        super(ElementView, self).__init__(parent)

        self.fr = QLabel(targetName)
        grid = QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)

class ProbeView(QFrame):
    def __init__(self, parent, targetName, probeId):
        super(ProbeView, self).__init__(parent)
