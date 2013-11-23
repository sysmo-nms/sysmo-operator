#!/usr/bin/env python
import  time
import  os
import  sys
import  pprint

from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    PySide.QtNetwork    import *
from    TkorderIcons        import TkorderIcons,TkorderImages
import  Supercast
import  ModTracker

_fromUtf8 = lambda s: s

class TkorderClient(QMainWindow):
    " The main tkorder window "
    def __init__(self, parent=None):
        super(TkorderClient, self).__init__(parent)
        TkorderIcons.init()
        TkorderImages.init()
        TkorderClient.singleton = self

        self.readSettings()

        " MainWindow "
        self.setObjectName(_fromUtf8("MainWindow"))

        " Tray icon "
        self.trayMenu = QMenu(self)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.setIcon(TkorderIcons.get('applications-development'))
        self.trayIcon.setVisible(True)

        " Status bar "
        self.statusBar = QStatusBar(self)
        #self.statusBar.setStyleSheet(
        #    "QStatusBar { \
        #        border: 1px solid black;\
        #        border-radius: 50px;\
        #        background: #B0C2D9 \
        #    }")
        self.setStatusBar(self.statusBar)


        " Menu bar "
        "File"
        exitAction  = QAction(
            TkorderIcons.get('system-log-out'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        debugAction  = QAction(
            TkorderIcons.get('applications-development'), '&Debug', self)
        debugAction.setShortcut('Ctrl+D')
        debugAction.triggered.connect(self.logTargets)
        menu        = self.menuBar()
        menuFile    = menu.addMenu('Engage')
        menuFile.addAction(exitAction)
        menuFile.addAction(debugAction)

        "Win"
        fullScreenAction  = QAction(
            TkorderIcons.get('video-display'), '&Full screen', self)
        fullScreenAction.setShortcut('Ctrl+F')
        fullScreenAction.triggered.connect(self.toggleFullScreen)
        menuWin     = menu.addMenu('Views')
        menuWin.addAction(fullScreenAction)


        " Server connexion and socket related "
        self.supercast = Supercast.Link(self)
        self.supercast.setSocketServer('localhost')
        self.supercast.setSocketPort(8888)

        " End init "
        self.setCentralWidget(
            TkorderCentralWidget(self))
        self.updateStatusBar("Started!")

    def toggleFullScreen(self):
        if self.isFullScreen() == False:
            self.showFullScreen()
        else:
            self.showNormal()
        
    def logTargets(self):
        pp  = pprint.PrettyPrinter(indent=4)
        d   = ModTracker.TrackerMain.singleton.targets
        print pp.pprint(d)

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)

    def getSettings(self):
        return self.config

    def readSettings(self):
        settings = QSettings("Kmars", "tkorder")
        self.config = settings 
        self.restoreGeometry(settings.value("TkorderMain/geometry"))
        self.restoreState(settings.value("TkorderMain/windowState"))

    def closeEvent(self, event):
        settings = QSettings("Kmars", "tkorder")
        settings.setValue("TkorderMain/geometry", self.saveGeometry())
        settings.setValue("TkorderMain/windowState", self.saveState())
        QMainWindow.closeEvent(self, event)

class TkorderCentralWidget(QFrame):
    def __init__(self, parent):
        super(TkorderCentralWidget, self).__init__(parent)
        grid        = QGridLayout(self)
        grid.setContentsMargins(5,9,9,9)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        grid.addWidget(LeftModSelector(self), 0,0,0,1)
        grid.addWidget(ModView(self),         0,1,1,1)
        self.setLayout(grid)

class LeftModSelector(QFrame):
    def __init__(self, parent):
        super(LeftModSelector, self).__init__(parent)
        self.setFixedWidth(30)
        grid        = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(5)
        mod1 = QLabel(self)
        mod2 = QLabel(self)
        mod1.setFrameShape(QFrame.StyledPanel)
        mod2.setFrameShape(QFrame.StyledPanel)
        grid.addWidget(mod1, 0,0)
        grid.addWidget(mod2, 1,0)
        self.setLayout(grid)
        #self.setFrameShape(QFrame.StyledPanel)

class ModView(QFrame):
    def __init__(self, parent):
        super(ModView, self).__init__(parent)
        grid        = QGridLayout(self)
        grid.setContentsMargins(5,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        modTracker  = ModTracker.TrackerMain(self)
        grid.addWidget(modTracker, 0, 0)
        self.setLayout(grid)

def main(arguments):
    tkorderApp    = QApplication(arguments)
    #fo = open('style/dib.stylesheet')
    #styleSheet = fo.read()
    #fo.close()
    #tkorderApp.setStyleSheet(styleSheet)
    tkorderUi     = TkorderClient()
    tkorderApp.setWindowIcon(
        TkorderIcons.get('applications-development')
    )

    #print QStyleFactory.keys()
    #tkorderApp.setStyle('Plastique')
    loginUi         = Supercast.LogInDialog2()
    loginUi.supercastClient = tkorderUi
    loginUi.show()

    sys.exit(tkorderApp.exec_())
