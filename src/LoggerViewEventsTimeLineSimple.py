from    PySide.QtGui        import *
from    PySide.QtCore       import *

class SimpleTimeLine(QFrame):
    def __init__(self, parent):
        super(SimpleTimeLine, self).__init__(parent)
        self.setBackgroundRole(QPalette.Base)
        grid = QGridLayout(self)
        grid.addWidget(QLabel('simple time line', self), 0,0)
        self.setLayout(grid)
