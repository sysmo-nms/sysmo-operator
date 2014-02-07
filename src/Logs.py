from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons

import  TkorderMain

class LogsMain(QFrame):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(LogsMain, self).__init__(parent)
        LogsMain.singleton = self

        grid = QGridLayout(self)
        grid.addWidget(QLabel('logs', self), 0,0)

        self.setLayout(grid)

    def toggleButtonClicked(self):
        print "toggle"
