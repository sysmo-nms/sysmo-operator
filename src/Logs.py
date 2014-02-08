from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Commercials

import  TkorderMain

class LogsMain(QFrame):
    def __init__(self, parent):
        super(LogsMain, self).__init__(parent)
        grid = self.initLogLayout()

        self.setLayout(grid)

    def initLogLayout(self):
        ad = Commercials.LogAd(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print "toggle"
