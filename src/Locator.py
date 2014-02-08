from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtSvg    import *
import  TkorderIcons
import  Commercials

import  TkorderMain

class LocatorMain(QFrame):
    def __init__(self, parent):
        super(LocatorMain, self).__init__(parent)
        LocatorMain.singleton = self
        self.enabled = False
        grid = self.initLocatorLayout()
        self.setLayout(grid)

    def initLocatorLayout(self):
        ad = Commercials.LocatorAd(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)
        

    def toggleButtonClicked(self):
        print "toggle"
