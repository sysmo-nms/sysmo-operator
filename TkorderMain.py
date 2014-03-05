#!/usr/bin/env python
import  time
import  os
import  sys
import  pprint

from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    PySide.QtNetwork    import *
from    MonitorDashboardArea    import *
from    TkorderIcons        import TkorderIcons,TkorderImages
from    TkorderDialog       import LogIn
import  Supercast
import  Monitor
import  Locator
import  Logs
import  Iphelper
import  Backup
import  MonitorProxyEvents

_fromUtf8 = lambda s: s

class TkorderClient(QMainWindow):

    " The main tkorder window "

    closeSignal = Signal()

    def __init__(self, parent=None):
        super(TkorderClient, self).__init__(parent)
        TkorderClient.singleton = self

        TkorderIcons.init()
        TkorderImages.init()

        self.readSettings()
        self.initMenus()

        # Server connexion and socket related
        self.supercast = Supercast.Link(self)
        self.supercast.setErrorHandler(self.socketEventHandler)

        # Widget layout
        self.central = TkorderCentralWidget(self)
        self.setCentralWidget(self.central)
        self.updateStatusBar("Started!")

    def addTopDockWidget(self, widget, name):
        newDock = QDockWidget(self)
        newDock.setObjectName(name)
        newDock.setAllowedAreas(Qt.TopDockWidgetArea)
        newDock.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetVerticalTitleBar)
        newDock.setWidget(widget)
        newDock.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        newDock.setContentsMargins(0,0,0,0)
        self.addDockWidget(Qt.TopDockWidgetArea,newDock,Qt.Horizontal)
        
    def initMenus(self):
        " MainWindow "
        self.setObjectName(_fromUtf8("MainWindow"))
        self.setWindowTitle('Noctopus')

        " Tray icon "
        #self.trayMenu = QMenu(self)
        self.trayIcon = QSystemTrayIcon(self)
        #self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.setIcon(TkorderIcons.get('applications-development'))
        self.trayIcon.setVisible(True)
        self.trayIcon.activated.connect(self._trayClic)

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

        actionSimpleView    = QAction('Simplified view', self)
        actionSimpleView.setCheckable(True)
        self.viewMode = 'simple'
        actionSimpleView.triggered.connect(self.setSimpleView)

        actionMinimalView    = QAction('Minimal view', self)
        actionMinimalView.setCheckable(True)
        actionMinimalView.triggered.connect(self.setMinimalView)

        actionExpertView    = QAction('Expert view', self)
        actionExpertView.setCheckable(True)
        actionExpertView.triggered.connect(self.setExpertView)
        actionExpertView.setChecked(True)

        toggleSimpleView    = QActionGroup(self)
        toggleSimpleView.addAction(actionMinimalView)
        toggleSimpleView.addAction(actionSimpleView)
        toggleSimpleView.addAction(actionExpertView)
        toggleSimpleView.setExclusive(True)

        menuWin     = menu.addMenu('Views')
        menuWin.addAction(actionMinimalView)
        menuWin.addAction(actionSimpleView)
        menuWin.addAction(actionExpertView)
        menuWin.addSeparator()
        menuWin.addAction(fullScreenAction)


        " configure menu "

        actionConfigureProxy = QAction('Proxy settings', self)
        actionConfigureProxy.triggered.connect(self.setProxySettings)

        menuConf    = menu.addMenu('Configure')
        menuConf.addAction(actionConfigureProxy)

    def setProxySettings(self):
        print "set proxy settings"

    def _trayClic(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            print self.isHidden()
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def setMinimalView(self):
        if self.viewMode != 'minimal':
            self.viewGeometry = self.saveGeometry()
            Monitor.MonitorMain.singleton.setMinimalView(True)
            self.setFixedWidth(400)
            self.viewMode = 'minimal'

    def setSimpleView(self):
        if self.viewMode == 'minimal':
            self.setMaximumSize(16777215,16777215)
            self.setMinimumSize(0,0)
            self.restoreGeometry(self.viewGeometry)
        Monitor.MonitorMain.singleton.setMinimalView(False)
        DashboardStack.singleton.setSimpleView()
        self.viewMode = 'simple'

    def setExpertView(self):
        if self.viewMode == 'minimal':
            self.setMaximumSize(16777215,16777215)
            self.setMinimumSize(0,0)
            self.restoreGeometry(self.viewGeometry)
        Monitor.MonitorMain.singleton.setMinimalView(False)
        DashboardStack.singleton.setExpertView()
        self.viewMode = 'expert'

    def setDpi(self, width, height):
        self.dpiWidth   = width
        self.dpiHeight  = height

    def toggleFullScreen(self):
        if self.isFullScreen() == False:
            self.showFullScreen()
        else:
            self.showNormal()
        
    def socketEventHandler(self, event):
        if   event == QAbstractSocket.ConnectionRefusedError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.RemoteHostClosedError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.HostNotFoundError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.SocketAccessError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.SocketResourceError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.SocketTimeoutError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.DatagramTooLargeError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.NetworkError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.AddressInUseError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.SocketAddressNotAvailableError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.UnsupportedSocketOperationError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.SslHandshakeFailedError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.UnfinishedSocketOperationError:
            self._showMessageBox(event)
        elif event == QAbstractSocket.UnknownSocketError:
            self._showMessageBox(event)
        else:
            self._showMessageBox(event)

    def _showMessageBox(self, event):
        msgBox = QMessageBox(self)
        msgBox.setText("Socket ERROR %s" % event)
        msgBox.setStandardButtons(QMessageBox.Close)
        msgBox.exec_()
        self.close()


    def logTargets(self):
        pp  = pprint.PrettyPrinter(indent=4)
        d   = MonitorProxyEvents.ChannelHandler.singleton.targets
        print pp.pprint(d)

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
        self.closeSignal.emit()
        settings = QSettings("Kmars", "tkorder")
        settings.setValue("TkorderMain/geometry",       self.saveGeometry())
        settings.setValue("TkorderMain/windowState",    self.saveState())
        self.central.modView.monitor.saveLayoutState()
        QMainWindow.closeEvent(self, event)




class TkorderCentralWidget(QFrame):
    def __init__(self, parent):
        super(TkorderCentralWidget, self).__init__(parent)
        grid        = QGridLayout(self)
        grid.setContentsMargins(5,9,9,9)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        self.modView        = TkorderStackedLayout(self)
        self.leftSelector   = LeftModSelector(self, self.modView)

        grid.addWidget(self.leftSelector,     0,0,0,1)
        grid.addWidget(self.modView,          0,1,1,1)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        self.leftSelector.connectAll()
        self.setLayout(grid)

class TkorderStackedLayout(QFrame):
    def __init__(self, parent):
        super(TkorderStackedLayout, self).__init__(parent)
        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(5,0,0,0)

        self.monitor = Monitor.MonitorMain(self)
        self.locator = Locator.LocatorMain(self)
        self.logs    = Logs.LogsMain(self)
        self.iphelper = Iphelper.IphelperMain(self)
        self.backup  = Backup.BackupMain(self)

        self.stack.addWidget(self.monitor)
        self.stack.addWidget(self.locator)
        self.stack.addWidget(self.logs)
        self.stack.addWidget(self.iphelper)
        self.stack.addWidget(self.backup)
        self.setLayout(self.stack)

    def goToLocator(self):
        self.stack.setCurrentWidget(self.locator)

    def goToMonitor(self):
        self.stack.setCurrentWidget(self.monitor)
    
    def goToLogs(self):
        self.stack.setCurrentWidget(self.logs)

    def goToIphelper(self):
        self.stack.setCurrentWidget(self.iphelper)

    def goToBackup(self):
        self.stack.setCurrentWidget(self.backup)

class LeftModSelector(QFrame):
    def __init__(self, parent, stackWidget):
        super(LeftModSelector, self).__init__(parent)
        self.stackWidget = stackWidget

        self.setFixedWidth(30)
        grid        = QGridLayout(self)
        self.setContentsMargins(0,0,0,0)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        buttonPol = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.monitor = QPushButton(self)
        self.monitor.setSizePolicy(buttonPol)
        self.monitor.setIconSize(QSize(30,100))
        self.monitor.setCheckable(True)
        self.monitor.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
        self.monitor.setChecked(True)

        self.locator = QPushButton(self)
        self.locator.setSizePolicy(buttonPol)
        self.locator.setIconSize(QSize(30,100))
        self.locator.setCheckable(True)
        self.locator.setIcon(TkorderIcons.get('utilities-system-monitor-black'))

        self.logs = QPushButton(self)
        self.logs.setSizePolicy(buttonPol)
        self.logs.setIconSize(QSize(30,100))
        self.logs.setCheckable(True)
        self.logs.setIcon(TkorderIcons.get('utilities-system-monitor-black'))

        self.iphelper = QPushButton(self)
        self.iphelper.setSizePolicy(buttonPol)
        self.iphelper.setIconSize(QSize(30,100))
        self.iphelper.setCheckable(True)
        self.iphelper.setIcon(TkorderIcons.get('utilities-system-monitor-black'))

        self.backup = QPushButton(self)
        self.backup.setSizePolicy(buttonPol)
        self.backup.setIconSize(QSize(30,100))
        self.backup.setCheckable(True)
        self.backup.setIcon(TkorderIcons.get('utilities-system-monitor-black'))

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.monitor)
        self.buttonGroup.addButton(self.locator)
        self.buttonGroup.addButton(self.logs)
        self.buttonGroup.addButton(self.iphelper)
        self.buttonGroup.addButton(self.backup)
        self.buttonGroup.setExclusive(True)

        grid.addWidget(self.monitor,    0,0)
        grid.addWidget(self.locator,    1,0)
        grid.addWidget(self.logs,       2,0)
        grid.addWidget(self.iphelper,   3,0)
        grid.addWidget(self.backup,     4,0)

        #self.backup = QPushButton(self)
        #self.backup.setSizePolicy(buttonPol)
        #self.backup.setIcon(TkorderIcons.get('emblem-system'))
        #grid.addWidget(self.backup, 1,0)
        self.currentView = 'monitor'
        self.setLayout(grid)

    def connectAll(self):
        self.monitor.clicked.connect(self.monitorClick)
        self.locator.clicked.connect(self.locatorClick)
        self.logs.clicked.connect(self.logsClick)
        self.iphelper.clicked.connect(self.iphelperClick)
        self.backup.clicked.connect(self.backupClick)

    def monitorClick(self):
        if self.currentView == 'monitor':
            Monitor.MonitorMain.singleton.toggleButtonClicked()
        else:
            self.currentView = 'monitor'
            self.stackWidget.goToMonitor()

    def locatorClick(self):
        if self.currentView == 'locator':
            Locator.LocatorMain.singleton.toggleButtonClicked()
        else:
            self.currentView = 'locator'
            self.stackWidget.goToLocator()
    
    def logsClick(self):
        if self.currentView == 'logs':
            Logs.LogsMain.singleton.toggleButtonClicked()
        else:
            self.currentView = 'logs'
            self.stackWidget.goToLogs()

    def iphelperClick(self):
        if self.currentView == 'iphelper':
            Iphelper.IphelperMain.singleton.toggleButtonClicked()
        else:
            self.currentView = 'iphelper'
            self.stackWidget.goToIphelper()

    def backupClick(self):
        if self.currentView == 'backup':
            Backup.BackupMain.singleton.toggleButtonClicked()
        else:
            self.currentView = 'backup'
            self.stackWidget.goToBackup()

  


def main(arguments):
    tkorderApp  = QApplication(arguments)
    screen_rect = tkorderApp.desktop().screenGeometry()
    width, height = screen_rect.width, screen_rect.height()
    #tkorderApp.setStyle('cde')
    tkorderUi   = TkorderClient()
    tkorderUi.setDpi(width, height)
    tkorderApp.setWindowIcon(TkorderIcons.get('applications-development'))
    loginUi     = LogIn()
    loginUi.supercastClient = tkorderUi
    loginUi.show()
    sys.exit(tkorderApp.exec_())
