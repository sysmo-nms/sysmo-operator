from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Commercials

import  TkorderMain

class IphelperMain(QFrame):
    def __init__(self, parent):
        super(IphelperMain, self).__init__(parent)
        grid = self.initIpHelper()
        self.setLayout(grid)

    def initIpHelper(self):
        ad = Commercials.IphelperAd(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print "toggle"
