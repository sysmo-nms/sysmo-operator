from    PySide.QtGui     import *

class ElementView(QFrame):
    def __init__(self, parent, targetName, probeId):
        super(ElementView, self).__init__(parent)
        self.fr = QLabel(targetName)
        grid = QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)
