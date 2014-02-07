from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons

import  TkorderMain

class LocatorMain(QFrame):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(LocatorMain, self).__init__(parent)
        LocatorMain.singleton = self

        grid = QGridLayout(self)
        grid.addWidget(QLabel('locator', self), 0,0)

        self.setLayout(grid)

    def toggleButtonClicked(self):
        print "toggle"
