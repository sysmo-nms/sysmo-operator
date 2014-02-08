from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Commercials

import  TkorderMain

class BackupMain(QFrame):
    def __init__(self, parent):
        super(BackupMain, self).__init__(parent)
        grid = self.initBackupLayout()
        self.setLayout(grid)

    def initBackupLayout(self):
        ad = Commercials.BackupAd(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print "toggle"
