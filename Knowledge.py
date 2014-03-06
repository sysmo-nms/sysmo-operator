from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Commercials

import  TkorderMain

class KnowledgeMain(QFrame):
    def __init__(self, parent):
        super(KnowledgeMain, self).__init__(parent)
        KnowledgeMain.singleton = self
        grid = self.initKnowledgeLayout()
        self.setLayout(grid)

    def initKnowledgeLayout(self):
        ad = Commercials.KnowledgeAd(self)
        grid = QGridLayout(self)
        grid.addWidget(ad, 0,0)

    def toggleButtonClicked(self):
        print "toggle"
