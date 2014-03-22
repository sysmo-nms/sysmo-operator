# python lib
from functools import partial

# PySide
from    PySide.QtNetwork import QAbstractSocket
from    PySide.QtCore   import (
    Qt,
    Signal,
    QSettings,
    QSize,
    QObject,
    QThread
)

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
    QMenu,
    QStackedLayout,
    QLabel,
    QToolButton,
    QMessageBox,
    QDrag
)


# local dependencies
from    noctopus_images     import getIcon, getImage, noctopusGraphicsInit
from    noctopus_dialogs    import Proxy

# supercast
from  supercast.main    import Supercast

# extentions
#import  Monitor.main
import  opus.locator.main
import  opus.logviewer.main
import  opus.iphelper.main
import  opus.scheduller.main
import  opus.knowledge.main


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

    willClose       = Signal()

    def __init__(self, parent=None):
        super(NMainWindow, self).__init__(parent)
        NMainWindow.singleton = self
        self.setObjectName('MainWindow')
        self.setWindowTitle('Noctopus')
        noctopusGraphicsInit()

        self._initProxySettings()
        self._initViewModes()
        self._initTray()

        self._initMenus()
        self._initStatusBar()
        self._initLayout()
        self._restoreSettings()
        self._initSupercast()

    #####################
    # CHILD MODULES API #
    #####################
    def getViewMode(self):
        return self._activeViewMode

    def getProxySettings(self):
        return self._activeProxySettings

    def setStatusMsg(self, msg):
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

    #########################
    # ProxySetting and      #
    # ProxySetting callback #
    #########################
    def _launchProxySettings(self):
        proxyUi = Proxy(self.setProxySettings, parent=self)
        
    def setProxySettings(self, proxySet):
        self._activeProxySettings = proxySet
        self.proxySettings.emit(self._activeProxySettings)

    ######################
    # Supercast CALLBACK #
    ######################
    def handleSupercastEvent(self, event):
        (key, payload) = event
        if    key == 'login_success':
            self._supercastLogged = True
            self.show()
        elif  key == 'abort':
            self.close()

    #########
    # INITS #
    #########
    def _initSupercast(self):
        eventHandler = self.handleSupercastEvent
        self._supercastLogged = False
        self._supercast = Supercast(self, eventHandler, mainwindow=self)
        self._supercast.tryLogin()

    def _initLayout(self):
        self._central = NCentralFrame(self)
        self.setCentralWidget(self._central)

    def _initProxySettings(self):
        proxySet = dict()
        proxySet['use']     = False
        proxySet['host']    = ''
        proxySet['port']    = 1
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
        self._statusBar = NStatusBar(self)
        self.setStatusBar(self._statusBar)

    def _initMenus(self):
        " Menu bar "
        "File"
        exitAction  = QAction(getIcon('system-log-out'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        menu        = self.menuBar()
        menuFile    = menu.addMenu('Noctopus')
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
            self._activeViewMode['screen'] = 'full'
            self.viewMode.emit(self._activeViewMode)
        else:
            self.showNormal()
            self._activeViewMode['screen'] = 'normal'
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
            if self._supercastLogged == False: return
            if self.isHidden():
                self.show()
                self._activeViewMode['tray'] = 'traymax'
                self.viewMode.emit(self._activeViewMode)
            else:
                self.hide()
                self._activeViewMode['tray'] = 'traymin'
                self.viewMode.emit(self._activeViewMode)

    #############
    # OVERLOADS #
    #############
    def closeEvent(self, event):
        self.willClose.emit()
        settings = QSettings("Noctopus NMS", "noctopus-client")
        settings.setValue("NMainWindow/geometry",       self.saveGeometry())
        settings.setValue("NMainWindow/windowState",    self.saveState())
        settings.setValue("NMainWindow/proxySettings",  self._activeProxySettings)
        settings.setValue("NMainWindow/viewMode",       self._activeViewMode)
        self._supercast.supercastClose()
        QMainWindow.closeEvent(self, event)

    ############
    # SETTINGS #
    ############
    def _restoreSettings(self):
        settings = QSettings("Noctopus NMS", "noctopus-client")
        self.restoreGeometry(settings.value("NMainWindow/geometry"))
        self.restoreState(settings.value("NMainWindow/windowState"))
        proxySet = settings.value("NMainWindow/proxySettings")
        if proxySet != None: self._activeProxySettings = proxySet
        #viewMode = settings.value("NMainWindow/viewMode")
        #if viewMode != None: self._activeViewMode = viewMode
        #activeOpus = ...


##############################################################################
class NStatusBar(QStatusBar):
    def __init__(self, parent):
        super(NStatusBar, self).__init__(parent)
        debugButton = QToolButton(self)
        debugButton.setIcon(getIcon('applications-development'))
        self.addPermanentWidget(debugButton)



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
class NSelectorButton(QPushButton):
    def __init__(self, parent):
        super(NSelectorButton, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(buttonPol)
        self.setIconSize(QSize(30,100))
        self.setCheckable(True)
        self._initMenu()

    def _initMenu(self):
        self._menu = QMenu(self)
        self._menu.addAction('Move up')
        self._menu.addAction('Move down')
        self._menu.addAction('Hide button')
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._menu.exec_(self.mapToGlobal(event.pos()))
        QPushButton.mousePressEvent(self, event)


class NSelector(QFrame):
    
    " left button ramp container "

    appButtonPressed = Signal(str)
    appButtonToggled = Signal(str)

    def __init__(self, parent, stackWidget):
        super(NSelector, self).__init__(parent)
        NSelector.singleton = self
        self._stackWidget   = stackWidget
        self.setFixedWidth(30)

        self._initButtons()
        self._initButtonGroup()
        self._initButtonSelector()
        self._initStack()

        self._gridAll()

    def _gridAll(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setVerticalSpacing(2)

        self.grid.addWidget(self.menuButton, 0,0)

        for key in self._buttons.keys():
            self.grid.addWidget(
                self._buttons[key]['widget'],
                self._buttons[key]['row'],
                0)
            self.grid.setRowStretch(self._buttons[key]['row'], 1)

        self.currentView = 'monitor'
        self.setLayout(self.grid)

    #################################
    # SHOW OR HIDE BUTTONS FUNCTION #
    #################################
    def _initButtonSelector(self):
        self.menuButton = QPushButton(self)
        self._menuHide  = QMenu(self)
        for key in self._buttons.keys():
            action = self._menuHide.addAction(key)
            action.setData(key)
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(partial(self._selectHide, key))
            self._buttons[key]['action'] = action
        self.menuButton.setMenu(self._menuHide)
        self.menuButton.setIcon(getIcon('emblem-system'))
        
    def _selectHide(self, key):
        if self._buttons[key]['action'].isChecked():
            self._showButton(key)
        else:
            self._hideButton(key)

    def _hideButton(self, key):
        wid     = self._buttons[key]['widget']
        row     = self._buttons[key]['row']
        wid.hide()
        self.grid.removeWidget(wid)
        self.grid.setRowStretch(row, 0)
        
    def _showButton(self, key):
        row     = self._buttons[key]['row']
        wid     = self._buttons[key]['widget']
        wid.show()
        self.grid.addWidget(wid, row, 0)
        self.grid.setRowStretch(row, 1)

##############################################################################
################# EXTENTION CONFIGURATION BEGIN ##############################
##############################################################################
# TODO use a configuration file
    def _initButtons(self):
        self._buttons = dict()
        self._buttons['monitor'] = dict()
        self._buttons['monitor']['row'] = 1
        self._buttons['monitor']['widget']    = NSelectorButton(self)
        self._buttons['monitor']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['locator'] = dict()
        self._buttons['locator']['row'] = 2
        self._buttons['locator']['widget']    = NSelectorButton(self)
        self._buttons['locator']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['logviewer'] = dict()
        self._buttons['logviewer']['row'] = 3
        self._buttons['logviewer']['widget']       = NSelectorButton(self)
        self._buttons['logviewer']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['iphelper'] = dict()
        self._buttons['iphelper']['row'] = 4
        self._buttons['iphelper']['widget']   = NSelectorButton(self)
        self._buttons['iphelper']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['scheduller'] = dict()
        self._buttons['scheduller']['row'] = 5
        self._buttons['scheduller']['widget']    = NSelectorButton(self)
        self._buttons['scheduller']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['knowledge'] = dict()
        self._buttons['knowledge']['row'] = 6
        self._buttons['knowledge']['widget']  = NSelectorButton(self)
        self._buttons['knowledge']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

    def _initStack(self):
        self.appButtonPressed.connect(self._stackWidget.selectEvent)

        #self._stackWidget.addLayer(opus.monitor.main.Central,    'monitor')
        self._stackWidget.addLayer(opus.locator.main.Central,    'locator')
        self._stackWidget.addLayer(opus.knowledge.main.Central,  'knowledge')
        self._stackWidget.addLayer(opus.iphelper.main.Central,   'iphelper')
        self._stackWidget.addLayer(opus.scheduller.main.Central, 'scheduller')
        self._stackWidget.addLayer(opus.logviewer.main.Central,  'logviewer')
##############################################################################
################# EXTENTION CONFIGURATION END ################################
##############################################################################


    def _initButtonGroup(self):
        self._buttons['monitor']['widget'].setChecked(True)
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)
        for key in self._buttons.keys():
            self.buttonGroup.addButton(self._buttons[key]['widget'])

    def connectAll(self):
        self.appButtonPressed.connect(self._stackWidget.selectEvent)
        for key in self._buttons.keys():
            but = self._buttons[key]['widget']
            but.clicked.connect(partial(self._appButtonPressed, key))
            
    def _appButtonPressed(self, app):
        if self.currentView == app:
            self.appButtonToggled.emit(app)
        else:
            self.appButtonPressed.emit(app)
            self.currentView = app



##############################################################################
class NCentralStack(QFrame):

    " main stack container "

    def __init__(self, parent):
        super(NCentralStack, self).__init__(parent)
        self._stack = QStackedLayout(self)
        self._stackElements = dict()
        self.setLayout(self._stack)

    def selectEvent(self, app):
        self._stack.setCurrentWidget(self._stackElements[app])

    def addLayer(self, pyCallable, app):
        qWidget = pyCallable(self)
        self._stackElements[app] = qWidget
        self._stack.addWidget(qWidget)
