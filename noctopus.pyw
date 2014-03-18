#!/usr/bin/env python2

# python lib
import  sys

# PySide
from    PySide.QtCore   import Signal
from    PySide.QtGui    import (
    QMainWindow,
    QApplication,
    QSystemTrayIcon,
    QAction,
    QActionGroup,
    QStatusBar,
    QFrame,
    QDockWidget
)

# dependencies
import  NoctopusImages
from    NoctopusImages  import getIcon, getImage
from    NoctopusDialogs import LogIn

# supercast
import  Supercast

# extentions
#import  Monitor
#import  Locator
#import  Logs
#import  Iphelper
#import  Scheduller
#import  Knowledge
#import  MonitorProxyEvents

class Noctopus(QMainWindow):

    " The main noctopus window "

    proxySettings   = Signal(dict)
    exitTriggered   = Signal()
    viewMode        = Signal(dict)
    # viewMode dict: {
    # 'screen': 'full' | 'normal',
    # 'mode':   'minimal' | 'simple' | 'expert',
    # 'tray': 'traymin', 'traymax'
    # }

    def __init__(self, parent=None):
        super(Noctopus, self).__init__(parent)
        Noctopus.singleton = self
        self.setObjectName('MainWindow')
        self.setWindowTitle('Noctopus')
        NoctopusImages.init()
        self._initMenus()
        self._initTray()
        self._initStatusBar()
        self._initViewModes()
        self._initProxySettings()
        self._initLayout()
        self._supercast = Supercast.Link(self)
        self._supercast.setErrorHandler(self.socketEventHandler)

#####################
# CHILD MODULES API #
#####################
    def getViewMode(self):
        return self._activeViewMode

    def getProxySettings(self):
        return self._activeProxySettings

    def setStatusMsg(self, msg):
        # TODO show log of msgs
        self._statusBar.showMessage(msg)

    def addTopDockWidget(self, widget, name):
        newDock = QDockWidget(self)
        newDock.setObjectName(name)
        newDock.setAllowedAreas(Qt.TopDockWidgetArea)
        newDock.setFeatures(
        QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetVerticalTitleBar
        )
        newDock.setWidget(widget)
        newDock.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        newDock.setContentsMargins(0,0,0,0)


#######################
# SUPERCAST CALLBACKS #
#######################
    def tryConnect(self, cred):
        self._supercast.userName = cred['name']
        self._supercast.userPass = cred['pass']
        self._supercast.server   = cred['server']
        self._supercast.port     = cred['port']
        self._supercast.tryConnect()
        self.show()
        return True

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

#########################
# SOCKET EVENT MESSAGES #
#########################
    def _showMessageBox(self, event):
        msgBox = QMessageBox(self)
        msgBox.setText("Socket ERROR %s" % event)
        msgBox.setStandardButtons(QMessageBox.Close)
        msgBox.exec_()
        self._terminateNoctopus()

#################
# VARIOUS INITS #
#################

    def _initProxySettings(self):
        proxySet = dict()
        proxySet['use']     = False
        proxySet['host']    = ''
        proxySet['port']    = 0
        self._activeProxySettings = proxySet

    def _initViewModes(self):
        self._activeViewMode = dict()
        self._activeViewMode['screen']   = "normal"
        self._activeViewMode['mode']     = "normal"
        self._activeViewMode['tray']     = "traymax"

    def _initTray(self):
        self._trayIcon = QSystemTrayIcon(self)
        self._trayIcon.setIcon(getIcon('applications-development'))
        self._trayIcon.setVisible(True)
        self._trayIcon.activated.connect(self._trayClic)

    def _initStatusBar(self):
        self._statusBar = QStatusBar(self)
        self.setStatusBar(self._statusBar)

    def _initMenus(self):
        " Menu bar "
        "File"
        exitAction  = QAction(getIcon('system-log-out'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self._terminateNoctopus)
        menu        = self.menuBar()
        menuFile    = menu.addMenu('Engage')
        menuFile.addAction(exitAction)

        "Win"
        fullScreenAction  = QAction(
            getIcon('video-display'), '&Full screen', self)
        fullScreenAction.setShortcut('Ctrl+F')
        fullScreenAction.triggered.connect(self._toggleFullScreen)

        actionSimpleView    = QAction('Simplified view', self)
        actionSimpleView.setCheckable(True)
        actionSimpleView.triggered.connect(self._setSimpleView)

        actionMinimalView    = QAction('Minimal view', self)
        actionMinimalView.setCheckable(True)
        actionMinimalView.triggered.connect(self._setMinimalView)

        actionExpertView    = QAction('Expert view', self)
        actionExpertView.setCheckable(True)
        actionExpertView.triggered.connect(self._setExpertView)
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
        actionConfigureProxy.triggered.connect(self._setProxySettings)

        menuConf    = menu.addMenu('Configure')
        menuConf.addAction(actionConfigureProxy)

###############
## VIEW MODES #
###############
    def _toggleFullScreen(self):
        if self.isFullScreen() == False:
            self.showFullScreen()
            self._activeViewMode['screen'] = "full"
            self.viewMode.emit(self._activeViewMode)
        else:
            self.showNormal()
            self._activeViewMode['screen'] = "normal"
            self.viewMode.emit(self._activeViewMode)

    def _setMinimalView(self):
        self._activeViewMode['mode'] = 'minimal'
        self.viewMode.emit(self._activeViewMode)

    def _setSimpleView(self):
        self._activeViewMode['mode'] = 'simple'
        self.viewMode.emit(self._activeViewMode)

    def _setExpertView(self):
        self._activeViewMode['mode'] = 'expert'
        self.viewMode.emit(self._activeViewMode)

    def _trayClic(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.show()
                self._activeViewMode['tray'] = 'traymax'
                self.viewMode.emit(self._activeViewMode)
            else:
                self.hide()
                self._activeViewMode['tray'] = 'traymin'
                self.viewMode.emit(self._activeViewMode)

#################
# CONFIGURATION #
#################
    def _setProxySettings(self, host, port, use):
        self._activeProxySettings['host']       = host
        self._activeProxySettings['port']       = port
        self._activeProxySettings['use']        = use
        self.proxySettings.emit(self._activeProxySettings)

        print "set proxy settings"

##########
# LAYOUT #
##########
    def _initLayout(self):
        self._central = CentralWidget(self)
        self.setCentralWidget(self._central)

#########
# UTILS #
#########
    def _terminateNoctopus(self):
        self.exitTriggered.emit()
        self.close()


class CentralWidget(QFrame):
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)

#         
# 
# 
# 
#         
# 
# 
# 
#     def logTargets(self):
#         pp  = pprint.PrettyPrinter(indent=4)
#         d   = MonitorProxyEvents.ChannelHandler.singleton.targets
#         print pp.pprint(d)
# 
# 
# 
#     def readSettings(self):
#         settings = QSettings("Kmars", "tkorder")
#         self.config = settings 
#         self.restoreGeometry(settings.value("TkorderMain/geometry"))
#         self.restoreState(settings.value("TkorderMain/windowState"))
# 
#     def closeEvent(self, event):
#         self.closeSignal.emit()
#         settings = QSettings("Kmars", "tkorder")
#         settings.setValue("TkorderMain/geometry",       self.saveGeometry())
#         settings.setValue("TkorderMain/windowState",    self.saveState())
#         self.central.modView.monitor.saveLayoutState()
#         QMainWindow.closeEvent(self, event)
# 
# 
# 
# 
# class TkorderCentralWidget(QFrame):
#     def __init__(self, parent):
#         super(TkorderCentralWidget, self).__init__(parent)
#         grid        = QGridLayout(self)
#         grid.setContentsMargins(5,9,9,9)
#         grid.setHorizontalSpacing(0)
#         grid.setVerticalSpacing(0)
# 
#         self.modView        = TkorderStackedLayout(self)
#         self.leftSelector   = LeftModSelector(self, self.modView)
# 
#         grid.addWidget(self.leftSelector,     0,0,0,1)
#         grid.addWidget(self.modView,          0,1,1,1)
#         grid.setColumnStretch(0, 0)
#         grid.setColumnStretch(1, 1)
#         self.leftSelector.connectAll()
#         self.setLayout(grid)
# 
# class TkorderStackedLayout(QFrame):
#     def __init__(self, parent):
#         super(TkorderStackedLayout, self).__init__(parent)
#         self.stack = QStackedLayout(self)
#         self.stack.setContentsMargins(5,0,0,0)
# 
#         self.monitor = Monitor.MonitorMain(self)
#         self.locator = Locator.LocatorMain(self)
#         self.logs    = Logs.LogsMain(self)
#         self.iphelper = Iphelper.IphelperMain(self)
#         self.shedule = Scheduller.SchedullerMain(self)
#         self.knowledge = Knowledge.KnowledgeMain(self)
# 
#         self.stack.addWidget(self.monitor)
#         self.stack.addWidget(self.locator)
#         self.stack.addWidget(self.logs)
#         self.stack.addWidget(self.iphelper)
#         self.stack.addWidget(self.shedule)
#         self.stack.addWidget(self.knowledge)
#         self.setLayout(self.stack)
# 
#     def goToLocator(self):
#         self.stack.setCurrentWidget(self.locator)
# 
#     def goToMonitor(self):
#         self.stack.setCurrentWidget(self.monitor)
#     
#     def goToLogs(self):
#         self.stack.setCurrentWidget(self.logs)
# 
#     def goToIphelper(self):
#         self.stack.setCurrentWidget(self.iphelper)
# 
#     def goToScheduller(self):
#         self.stack.setCurrentWidget(self.shedule)
# 
#     def goToKnowledge(self):
#         self.stack.setCurrentWidget(self.knowledge)
# 
# class LeftModSelector(QFrame):
#     def __init__(self, parent, stackWidget):
#         super(LeftModSelector, self).__init__(parent)
#         self.stackWidget = stackWidget
# 
#         self.setFixedWidth(30)
#         grid        = QGridLayout(self)
#         self.setContentsMargins(0,0,0,0)
#         grid.setContentsMargins(0,0,0,0)
#         grid.setHorizontalSpacing(0)
#         grid.setVerticalSpacing(0)
# 
#         buttonPol = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# 
#         self.monitor = QPushButton(self)
#         self.monitor.setSizePolicy(buttonPol)
#         self.monitor.setIconSize(QSize(30,100))
#         self.monitor.setCheckable(True)
#         self.monitor.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
#         self.monitor.setChecked(True)
# 
#         self.locator = QPushButton(self)
#         self.locator.setSizePolicy(buttonPol)
#         self.locator.setIconSize(QSize(30,100))
#         self.locator.setCheckable(True)
#         self.locator.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
# 
#         self.logs = QPushButton(self)
#         self.logs.setSizePolicy(buttonPol)
#         self.logs.setIconSize(QSize(30,100))
#         self.logs.setCheckable(True)
#         self.logs.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
# 
#         self.iphelper = QPushButton(self)
#         self.iphelper.setSizePolicy(buttonPol)
#         self.iphelper.setIconSize(QSize(30,100))
#         self.iphelper.setCheckable(True)
#         self.iphelper.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
# 
#         self.shedule = QPushButton(self)
#         self.shedule.setSizePolicy(buttonPol)
#         self.shedule.setIconSize(QSize(30,100))
#         self.shedule.setCheckable(True)
#         self.shedule.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
# 
#         self.knowledge = QPushButton(self)
#         self.knowledge.setSizePolicy(buttonPol)
#         self.knowledge.setIconSize(QSize(30,100))
#         self.knowledge.setCheckable(True)
#         self.knowledge.setIcon(TkorderIcons.get('utilities-system-monitor-black'))
# 
#         self.buttonGroup = QButtonGroup(self)
#         self.buttonGroup.addButton(self.monitor)
#         self.buttonGroup.addButton(self.locator)
#         self.buttonGroup.addButton(self.logs)
#         self.buttonGroup.addButton(self.iphelper)
#         self.buttonGroup.addButton(self.shedule)
#         self.buttonGroup.addButton(self.knowledge)
#         self.buttonGroup.setExclusive(True)
# 
#         grid.addWidget(self.monitor,    0,0)
#         grid.addWidget(self.locator,    1,0)
#         grid.addWidget(self.iphelper,   2,0)
#         grid.addWidget(self.knowledge,  3,0)
#         grid.addWidget(self.logs,       4,0)
#         grid.addWidget(self.shedule,    5,0)
# 
#         self.currentView = 'monitor'
#         self.setLayout(grid)
# 
#     def connectAll(self):
#         self.monitor.clicked.connect(self.monitorClick)
#         self.locator.clicked.connect(self.locatorClick)
#         self.logs.clicked.connect(self.logsClick)
#         self.iphelper.clicked.connect(self.iphelperClick)
#         self.shedule.clicked.connect(self.sheduleClick)
#         self.knowledge.clicked.connect(self.knowledgeClick)
# 
#     def monitorClick(self):
#         if self.currentView == 'monitor':
#             Monitor.MonitorMain.singleton.toggleButtonClicked()
#         else:
#             self.currentView = 'monitor'
#             self.stackWidget.goToMonitor()
# 
#     def locatorClick(self):
#         if self.currentView == 'locator':
#             Locator.LocatorMain.singleton.toggleButtonClicked()
#         else:
#             self.currentView = 'locator'
#             self.stackWidget.goToLocator()
#     
#     def logsClick(self):
#         if self.currentView == 'logs':
#             Logs.LogsMain.singleton.toggleButtonClicked()
#         else:
#             self.currentView = 'logs'
#             self.stackWidget.goToLogs()
# 
#     def iphelperClick(self):
#         if self.currentView == 'iphelper':
#             Iphelper.IphelperMain.singleton.toggleButtonClicked()
#         else:
#             self.currentView = 'iphelper'
#             self.stackWidget.goToIphelper()
# 
#     def sheduleClick(self):
#         if self.currentView == 'sheduller':
#             Scheduller.SchedullerMain.singleton.toggleButtonClicked()
#         else:
#             self.currentView = 'sheduller'
#             self.stackWidget.goToScheduller()
# 
#     def knowledgeClick(self):
#         if self.currentView == 'knowledge':
#             Knowledge.KnowledgeMain.singleton.toggleButtonClicked()
#         else:
#             self.currentView = 'knowledge'
#             self.stackWidget.goToKnowledge()
#   
# 
# 

if __name__ == '__main__':
    noctopusApp     = QApplication(sys.argv)
    noctopus        = Noctopus()
    noctopus.setWindowIcon(getIcon('applications-development'))
    loginUi         = LogIn(noctopus.tryConnect)
    loginUi.setWindowIcon(getIcon('applications-development'))

    loginUi.show()
    sys.exit(noctopusApp.exec_())
