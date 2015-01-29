from    PyQt4.QtGui    import *
from    PyQt4.QtCore   import *
from    .LocatorProxyEvents import ChannelHandler
import  Commercials

import  TkorderMain

class LocatorMain(QFrame):
    def __init__(self, parent):
        super(LocatorMain, self).__init__(parent)
        LocatorMain.singleton = self
        #self.enabled = False
        self.eventHandler   = ChannelHandler(self)
        self.enabled = True
        grid = self.initLocatorLayout()
        self.setLayout(grid)

    def initLocatorLayout(self):
        if self.enabled == False:
            ad      = Commercials.LocatorAd(self)
            grid    = QGridLayout(self)
            grid.addWidget(ad, 0,0)
        elif self.enabled == True:
            lab  = QLabel('locator', self)
            grid = QGridLayout(self)
            grid.addWidget(lab)
        

    def toggleButtonClicked(self):
        print("toggle")
