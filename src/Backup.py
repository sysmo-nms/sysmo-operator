from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons

import  TkorderMain

class BackupMain(QFrame):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(BackupMain, self).__init__(parent)
        BackupMain.singleton = self

        grid = QGridLayout(self)
        grid.addWidget(QLabel('Backup', self), 0,0)

        self.setLayout(grid)

    def toggleButtonClicked(self):
        print "toggle"
