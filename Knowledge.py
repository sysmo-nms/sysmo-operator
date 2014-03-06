from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtWebKit import *
import  Commercials

import  TkorderMain

class KnowledgeMain(QFrame):
    def __init__(self, parent):
        super(KnowledgeMain, self).__init__(parent)
        KnowledgeMain.singleton = self
        #self.enabled = False
        self.enabled = True
        grid = self.initKnowledgeLayout()
        self.setLayout(grid)

    def initKnowledgeLayout(self):
        if self.enabled == False:
            ad      = Commercials.KnowledgeAd(self)
            grid    = QGridLayout(self)
            grid.addWidget(ad, 0,0)
        elif self.enabled == True:
            wiki = KnowledgeApp(self)
            grid = QGridLayout(self)
            grid.addWidget(wiki)
        

    def toggleButtonClicked(self):
        print "toggle"

class KnowledgeApp(QFrame):
    def __init__(self, parent):
        super(KnowledgeApp, self).__init__(parent)
        grid = QGridLayout(self)
        self.setContentsMargins(0,0,0,0)
        grid.setContentsMargins(0,0,0,0)

        server  = 'localhost'

        wiki = QWebView(self)
        wiki.load(QUrl("http://%s:8080/wiki_base.html" % server))

        grid.addWidget(wiki,        0,0)
        self.setLayout(grid)









