from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons

import  TkorderMain

class IphelperMain(QFrame):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(IphelperMain, self).__init__(parent)
        IphelperMain.singleton = self

        grid = QGridLayout(self)
        grid.addWidget(QLabel('iphelper', self), 0,0)

        self.setLayout(grid)

    def toggleButtonClicked(self):
        print "toggle"
