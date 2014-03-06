from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Commercials

import  TkorderMain

class SchedullerMain(QFrame):
    def __init__(self, parent):
        super(SchedullerMain, self).__init__(parent)
        SchedullerMain.singleton = self
        grid = self.initSchedullerLayout()
        self.setLayout(grid)

    def initSchedullerLayout(self):
        ad = Commercials.SchedullerAd(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print "toggle"
