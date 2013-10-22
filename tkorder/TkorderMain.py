#!/usr/bin/env python
import  time
import  sys

from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    PySide.QtNetwork    import *
from    TkorderIcons        import TkorderIcons
#from    SupercastPDU        import decode, encode
import  Supercast
import  ModTracker
import  ModTracker.TrackerMain

_fromUtf8 = lambda s: s

class TkorderClient(QMainWindow):

    def __init__(self, parent=None):
        super(TkorderClient, self).__init__(parent)
        TkorderIcons.init()
        TkorderClient.singleton = self


        self.readSettings()
        " MainWindow "
        self.setObjectName(_fromUtf8("MainWindow"))
        #self.resize(1200, 600)
        #self.setMinimumSize(1000,500)

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
        exitAction  = QAction(
            TkorderIcons.get('system-log-out'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        menu        = self.menuBar()
        menuFile    = menu.addMenu('Engage')
        menuFile.addAction(exitAction)

        " Server connexion and socket related "
        self.supercast = Supercast.Link(self)
        self.supercast.setSocketServer('localhost')
        self.supercast.setSocketPort(8888)

        " End init "
        self.setCentralWidget(
            TkorderCentralWidget(self))
        self.updateStatusBar("Started!")

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)

    def readSettings(self):
        settings = QSettings("Kmars", "tkorder")
        print settings.value("geometry")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))

    def closeEvent(self, event):
        settings = QSettings("Kmars", "tkorder")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        print self.saveGeometry()
        QMainWindow.closeEvent(self, event)

class TkorderCentralWidget(QFrame):
    def __init__(self, parent):
        super(TkorderCentralWidget, self).__init__(parent)

        layout      = QGridLayout()
        modTracker  = ModTracker.TrackerMain.TrackerWindow(self)
        layout.addWidget(modTracker, 0, 0)

        self.setLayout(layout)

def main(arguments):
    tkorderApp    = QApplication(arguments)
    tkorderUi     = TkorderClient()
    tkorderApp.setWindowIcon(
        TkorderIcons.get('applications-development')
    )
    loginUi         = Supercast.LogInDialog2()
    loginUi.supercastClient = tkorderUi
    loginUi.show()

    sys.exit(tkorderApp.exec_())
