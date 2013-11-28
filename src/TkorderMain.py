#!/usr/bin/env python
import  time
import  os
import  sys
import  pprint

from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    PySide.QtNetwork    import *
from    TkorderIcons        import TkorderIcons,TkorderImages
from    TkorderDialog       import LogIn
import  Supercast
import  Monitor

_fromUtf8 = lambda s: s

class TkorderClient(QMainWindow):
    " The main tkorder window "
    def __init__(self, parent=None):
        super(TkorderClient, self).__init__(parent)
        TkorderClient.singleton = self

        TkorderIcons.init()
        TkorderImages.init()

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
        #debugAction.triggered.connect(self.logTargets)
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

        " End init "
        self.setCentralWidget(TkorderCentralWidget(self))
        self.updateStatusBar("Started!")

    def toggleFullScreen(self):
        if self.isFullScreen() == False:
            self.showFullScreen()
        else:
            self.showNormal()
        
    #def logTargets(self):
        #pp  = pprint.PrettyPrinter(indent=4)
        #d   = ModTracker.TrackerMain.singleton.targets
        #print pp.pprint(d)

    def tryConnect(self, cred):
        self.supercast.userName = cred['name']
        self.supercast.userPass = cred['pass']
        self.supercast.server   = cred['server']
        self.supercast.port     = cred['port']
        self.supercast.tryConnect()

        self.show()
        return True

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)

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
        self.leftSelector   = LeftModSelector(self)
        self.modView        = ModView(self)
        grid.addWidget(self.leftSelector,     0,0,0,1)
        grid.addWidget(self.modView,          0,1,1,1)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        self.leftSelector.connectAll()
        self.setLayout(grid)

class LeftModSelector(QFrame):
    def __init__(self, parent):
        super(LeftModSelector, self).__init__(parent)
        self.setFixedWidth(30)
        grid        = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(5)

        buttonPol = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.mod1 = QPushButton(self)
        self.mod1.setSizePolicy(buttonPol)
        self.mod1.setIconSize(QSize(30,100))
        self.mod1.setCheckable(True)
        self.mod1.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
        grid.addWidget(self.mod1, 0,0)

        #self.mod2 = QPushButton(self)
        #self.mod2.setSizePolicy(buttonPol)
        #self.mod2.setIcon(TkorderIcons.get('emblem-system'))
        #grid.addWidget(self.mod2, 1,0)

        self.setLayout(grid)

    def connectAll(self):
        mod1Toggle = Monitor.MonitorMain.singleton.toggleButtonClicked
        self.mod1.clicked.connect(mod1Toggle)

class ModView(QFrame):
    def __init__(self, parent):
        super(ModView, self).__init__(parent)
        grid        = QGridLayout(self)
        grid.setContentsMargins(5,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        monitor = Monitor.MonitorMain(self)
        grid.addWidget(monitor, 0, 0)
        self.setLayout(grid)

def main(arguments):
    tkorderApp  = QApplication(arguments)
    tkorderUi   = TkorderClient()
    tkorderApp.setWindowIcon(TkorderIcons.get('applications-development'))
    loginUi     = LogIn()
    loginUi.supercastClient = tkorderUi
    loginUi.show()
    sys.exit(tkorderApp.exec_())
