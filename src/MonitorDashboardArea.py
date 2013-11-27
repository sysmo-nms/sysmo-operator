from    PySide.QtGui        import *
from    PySide.QtCore       import *

class Dash(QFrame):

    def __init__(self, parent):
        super(Dash, self).__init__(parent)
        self.stackDict  = dict()
        grid = QGridLayout(self)
        grid.addWidget(QLabel('helll', self), 0,0)
        self.setLayout(grid)
