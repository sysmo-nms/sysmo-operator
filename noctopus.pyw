#!/usr/bin/env python2

# python lib
import  sys

# PySide
from    PySide.QtCore   import Signal, QSettings, QSize
from    PySide.QtGui    import (
    QMainWindow,
    QApplication,
    QSystemTrayIcon,
    QAction,
    QActionGroup,
    QStatusBar,
    QFrame,
    QDockWidget,
    QGridLayout,
    QSizePolicy,
    QPushButton,
    QButtonGroup,
    QMenu
)

# local dependencies
from    NoctopusImages  import getIcon, getImage, noctopusGraphicsInit
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

######################
# MODULES API HELPER #
######################
def nGetProxySettings():
    return NMainWindow.singleton.getProxySettings()

def nGetViewMode():
    return NMainWindow.singleton.getViewMode()

def nGetIcon(iconName):
    return getIcon(iconName)

def nGetImage(imageName):
    return getIcon(imageName)

def nConnectProxySettings(pyScallable):
    return NMainWindow.singleton.proxySettings.connect(pyScallable)

def nConnectViewMode(pyScallable):
    return NMainWindow.singleton.viewMode.connect(pyScallable)

def nSetStatusMsg(msg):
    return NMainWindow.singleton.setStatusMsg(msg)




##############################################################################
####################### CLASS DEFINITION #####################################
##############################################################################
class NMainWindow(QMainWindow):

    " The noctopus QMainWindow "

    proxySettings   = Signal(dict)
    # emit self._activeProxySettings dict: {
    #   'use':  True | False,
    #   'host': str,
    #   'port': int
    # }

    viewMode        = Signal(dict)
    # emit self._activeViewMode dict: {
    #   'screen':   'full' | 'normal',
    #   'mode':     'minimal' | 'simple' | 'expert',
    #   'tray':     'traymin' | 'traymax'
    # }

    def __init__(self, parent=None):
        super(NMainWindow, self).__init__(parent)
        NMainWindow.singleton = self
        self.setObjectName('MainWindow')
        self.setWindowTitle('Noctopus')
        noctopusGraphicsInit()
        self._initMenus()
        self._initTray()
        self._initStatusBar()
        self._initViewModes()
        self._initProxySettings()
        self._initLayout()
        self._supercast = Supercast.Link(self)
        self._supercast.setErrorHandler(self.socketEventHandler)
        self._restoreSettings()

    #####################
    # CHILD MODULES API #
    #####################
    def getViewMode(self):
        return self._activeViewMode

    def getProxySettings(self):
        return self._activeProxySettings

    def setStatusMsg(self, msg):
        # TODO show log of msgs button
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

    #########################################
    # NoctopusDialogs.ProxySetting and      #
    # NoctopusDialogs.ProxySetting CALLBACK #
    #########################################
    def _launchProxySettings(self):
        # TODO
        # dialog = NoctopusDialogs.ProxySettings(self, self.setProxySettings)
        # dialog.show()
        pass
        
    def setProxySettings(self, host, port, use):
        self._activeProxySettings['host']       = host
        self._activeProxySettings['port']       = port
        self._activeProxySettings['use']        = use
        self.proxySettings.emit(self._activeProxySettings)

        print "set proxy settings"

    ##################################
    # NoctopusDialogs.LogIn CALLBACK #
    ##################################
    def tryConnect(self, cred):
        self._supercast.userName = cred['name']
        self._supercast.userPass = cred['pass']
        self._supercast.server   = cred['server']
        self._supercast.port     = cred['port']
        self._supercast.tryConnect()
        self.show()
        return True

    ############################
    # Supercast.Link CALLBACKS #
    ############################
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
        exitAction.triggered.connect(self.close)
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
        actionConfigureProxy.triggered.connect(self._launchProxySettings)

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

    ##########
    # LAYOUT #
    ##########
    def _initLayout(self):
        self._central = NCentralFrame(self)
        self.setCentralWidget(self._central)

    #############
    # OVERLOADS #
    #############
    def closeEvent(self, event):
        settings = QSettings("Noctopus NMS", "noctopus-client")
        settings.setValue("NMainWindow/geometry",       self.saveGeometry())
        settings.setValue("NMainWindow/windowState",    self.saveState())
        QMainWindow.closeEvent(self, event)

    ############
    # SETTINGS #
    ############
    def _restoreSettings(self):
        settings = QSettings("Noctopus NMS", "noctopus-client")
        self._config = settings 
        self.restoreGeometry(settings.value("NMainWindow/geometry"))
        self.restoreState(settings.value("NMainWindow/windowState"))



##############################################################################
class NCentralFrame(QFrame):

    " central widget container "

    def __init__(self, parent):
        super(NCentralFrame, self).__init__(parent)
        grid = QGridLayout(self)
        self.centralStack   = NCentralStack(self)
        self.selector       = NSelector(self, self.centralStack)
        grid.addWidget(self.selector,       0,0,0,1)
        grid.addWidget(self.centralStack,   0,1,1,1)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        self.selector.connectAll()
        self.setLayout(grid)



##############################################################################
class NCentralStack(QFrame):

    " main stack container "

    def __init__(self, parent):
        super(NCentralStack, self).__init__(parent)



##############################################################################
class NSelectorButton(QPushButton):
    def __init__(self, parent):
        super(NSelectorButton, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(buttonPol)
        self.setIconSize(QSize(30,100))
        self.setCheckable(True)

class NSelector(QFrame):
    
    " left button ramp container "

    def __init__(self, parent, stackWidget):
        super(NSelector, self).__init__(parent)
        self._stackWidget   = stackWidget
        self.setFixedWidth(30)

        self._initButtonSelector()
        self._initButtons()
        self._initButtonGroup()

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setVerticalSpacing(2)

        grid.addWidget(self.menuButton, 0,0)

        grid.addWidget(self.monitor,    1,0)
        grid.addWidget(self.locator,    2,0)
        grid.addWidget(self.iphelper,   3,0)
        grid.addWidget(self.knowledge,  4,0)
        grid.addWidget(self.logs,       5,0)
        grid.addWidget(self.shedule,    6,0)

        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,1)
        grid.setRowStretch(5,1)
        grid.setRowStretch(6,1)

        self.currentView = 'monitor'
        self.setLayout(grid)

    def _initButtonSelector(self):
        self.menuButton = QPushButton(self)
        menu = QMenu(self)
        # TODO menu, select buttons we want to hide
        self.menuButton.setMenu(menu)
        self.menuButton.setIcon(getIcon('emblem-system'))
        

    def _initButtons(self):
        self.monitor    = NSelectorButton(self)
        self.monitor.setIcon(getIcon('utilities-system-monitor-black'))

        self.locator    = NSelectorButton(self)
        self.locator.setIcon(getIcon('utilities-system-monitor-black'))

        self.logs       = NSelectorButton(self)
        self.logs.setIcon(getIcon('utilities-system-monitor-black'))

        self.iphelper   = NSelectorButton(self)
        self.iphelper.setIcon(getIcon('utilities-system-monitor-black'))

        self.shedule    = NSelectorButton(self)
        self.shedule.setIcon(getIcon('utilities-system-monitor-black'))

        self.knowledge  = NSelectorButton(self)
        self.knowledge.setIcon(getIcon('utilities-system-monitor-black'))

    def _initButtonGroup(self):
        self.monitor.setChecked(True)
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.monitor)
        self.buttonGroup.addButton(self.locator)
        self.buttonGroup.addButton(self.logs)
        self.buttonGroup.addButton(self.iphelper)
        self.buttonGroup.addButton(self.shedule)
        self.buttonGroup.addButton(self.knowledge)
        self.buttonGroup.setExclusive(True)

        
    def connectAll(self): pass

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
# 
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

if __name__ == '__main__':
    noctopusApp     = QApplication(sys.argv)
    noctopus        = NMainWindow()
    noctopus.setWindowIcon(getIcon('applications-development'))
    loginUi         = LogIn(noctopus.tryConnect)
    loginUi.setWindowIcon(getIcon('applications-development'))

    loginUi.show()
    sys.exit(noctopusApp.exec_())
