from    PySide.QtGui        import *
from    PySide.QtCore       import *

class Dash(QTabWidget):

    def __init__(self, parent):
        super(Dash, self).__init__(parent)
        self.stackDict  = dict()
        #grid = QGridLayout(self)
        #grid.addWidget(QLabel('helll', self), 0,0)
        #grid.addWidget(QListView(self), 0,0)
        self.addTab(QListView(self), 'Default')
        self.addTab(QLabel('hell', self), 'Multiple document interface')
        self.addTab(QLabel('hell', self), 'Mapping')
        #self.setLayout(grid)
