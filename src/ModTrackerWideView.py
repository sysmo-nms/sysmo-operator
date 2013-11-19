from PySide.QtGui   import *
from PySide.QtCore  import *

class View(QFrame):
    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.fr = QLabel("WIDEVIEW")
        grid = QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)
