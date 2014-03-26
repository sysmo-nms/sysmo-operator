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
    QDockWidget,
    QSizePolicy,
    QPushButton,
    QButtonGroup,
    QMenu,
    QStackedLayout,
    QLabel,
    QToolButton,
    QMessageBox
)


# local dependencies
from    noctopus_images     import getIcon, noctopusGraphicsInit
from    noctopus_dialogs    import Proxy
from    noctopus_statusbar  import NStatusBar
from    noctopus_centerwidget   import NCentralFrame

# supercast
from  supercast.main    import Supercast


class NMainWindow(QMainWindow):

    " The noctopus QMainWindow "

    proxySettings   = Signal(dict)
    # emit self.activeProxySettings dict: {
    #   'use':  True | False,
    #   'host': str,
    #   'port': int
    # }

    viewMode        = Signal(dict)
    # emit self.activeViewMode dict: {
    #   'screen':   'full' | 'normal',
    #   'mode':     'minimal' | 'simple' | 'expert',
    #   'tray':     'traymin' | 'traymax'
    # }

    willClose       = Signal()
    # emit when the application will close

    supercastEnabled = Signal()
    # emit when supercast is enabled

    def __init__(self, style, parent=None):
        super(NMainWindow, self).__init__(parent)
        NMainWindow.singleton   = self
        self._noctopusStyle     = style
        noctopusGraphicsInit()

        self.setObjectName('MainWindow')
        self.setWindowIcon(getIcon('applications-development'))
        self.setWindowTitle('Noctopus')

        self._initSupercast()

        self._initProxySettings()
        self._initViewModes()
        self._initTray()

        self._initStatusBar()
        self._restoreSettings()
        self._initLayout()
        self._initMenus()


    #########
    # INITS #
    #########

    # Supercast
    def _initSupercast(self):
        self.supercastLogged = False
        self.supercast = Supercast(self, mainwindow=self)
        self.supercast.eventSignals.connect(self._handleSupercastEvents)
        self.supercast.tryLogin()

    def _handleSupercastEvents(self, event):
        (key, payload) = event
        if    key == 'success':
            self._supercastLogged = True
            self.supercastEnabled.emit()
            self.show()
        elif  key == 'abort':
            self.close()

    # Layout
    def _initLayout(self):
        self._central = NCentralFrame(self)
        self.setCentralWidget(self._central)

    # Proxy
    def _initProxySettings(self):
        proxySet = dict()
        proxySet['use']     = False
        proxySet['host']    = ''
        proxySet['port']    = 1
        self.activeProxySettings = proxySet

    # Views
    def _initViewModes(self):
        self.activeViewMode = dict()
        self.activeViewMode['screen']   = "normal"
        self.activeViewMode['mode']     = "normal"
        self.activeViewMode['tray']     = "traymax"

    # Tray
    def _initTray(self):
        self._trayIcon = QSystemTrayIcon(self)
        self._trayIcon.setIcon(getIcon('applications-development'))
        self._trayIcon.setVisible(True)
        self._trayIcon.activated.connect(self._trayClic)

    # Status
    def _initStatusBar(self):
        self.statusBar = NStatusBar(self)
        self.setStatusBar(self.statusBar)

    # Menus

    ###############
    ## VIEW MODES #
    ###############
    def _toggleFullScreen(self):
        if self.isFullScreen() == False:
            self.showFullScreen()
            self.activeViewMode['screen'] = 'full'
            self.viewMode.emit(self.activeViewMode)
        else:
            self.showNormal()
            self.activeViewMode['screen'] = 'normal'
            self.viewMode.emit(self.activeViewMode)

    def _setMinimalView(self):
        self.activeViewMode['mode'] = 'minimal'
        self.viewMode.emit(self.activeViewMode)

    def _setSimpleView(self):
        self.activeViewMode['mode'] = 'simple'
        self.viewMode.emit(self.activeViewMode)

    def _setExpertView(self):
        self.activeViewMode['mode'] = 'expert'
        self.viewMode.emit(self.activeViewMode)

    def _trayClic(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self._supercastLogged == False: return
            if self.isHidden():
                self.show()
                self.activeViewMode['tray'] = 'traymax'
                self.viewMode.emit(self.activeViewMode)
            else:
                self.hide()
                self.activeViewMode['tray'] = 'traymin'
                self.viewMode.emit(self.activeViewMode)

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

    ##########
    # STYLES #
    ##########
    def _setStyle(self, style):
        self._noctopusStyle = style
        msgBox = QMessageBox(self)
        msgBox.setText(self.tr('The application must restart to take your modification in consideration'))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    ###########
    # DIALOGS #
    ###########
    def _launchProxySettings(self):
        proxyUi = Proxy(self._setProxySettings, parent=self)
        
    def _setProxySettings(self, proxySet):
        self.activeProxySettings = proxySet
        self.proxySettings.emit(self.activeProxySettings)


    #############
    # OVERLOADS #
    #############
    def closeEvent(self, event):
        self.willClose.emit()
        settings = QSettings("Noctopus NMS", "noctopus-client")
        settings.setValue("NMainWindow/geometry",       self.saveGeometry())
        settings.setValue("NMainWindow/windowState",    self.saveState())
        settings.setValue("NMainWindow/proxySettings",  self.activeProxySettings)
        settings.setValue("NMainWindow/viewMode",       self.activeViewMode)
        settings.setValue("NMainWindow/style",          self._noctopusStyle)
        self.supercast.supercastClose()
        QMainWindow.closeEvent(self, event)

    ############
    # SETTINGS #
    ############
    def _restoreSettings(self):
        settings = QSettings("Noctopus NMS", "noctopus-client")

        self.restoreGeometry(settings.value("NMainWindow/geometry"))
        self.restoreState(settings.value("NMainWindow/windowState"))

        proxySet = settings.value("NMainWindow/proxySettings")
        if proxySet != None: self.activeProxySettings = proxySet

        #viewMode = settings.value("NMainWindow/viewMode")
        #if viewMode != None: self.activeViewMode = viewMode
        #activeOpus = ...

    #########
    # MENUS #
    #########
    def _initMenus(self):
        " Menu bar "
        "File"
        menu = self.menuBar()
        menuFile    = menu.addMenu('Noctopus')
        exitAction  = QAction(getIcon('system-log-out'), self.tr('&Exit'), self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        menuFile.addAction(exitAction)
    
        "Win"
        fullScreenAction  = QAction(
            getIcon('video-display'), self.tr('&Full screen'), self)
        fullScreenAction.setShortcut('Ctrl+F')
        fullScreenAction.triggered.connect(self._toggleFullScreen)
    
        actionSimpleView    = QAction(self.tr('Simplified view'), self)
        actionSimpleView.setCheckable(True)
        actionSimpleView.triggered.connect(self._setSimpleView)
    
        actionMinimalView    = QAction(self.tr('Minimal view'), self)
        actionMinimalView.setCheckable(True)
        actionMinimalView.triggered.connect(self._setMinimalView)
    
        actionExpertView    = QAction(self.tr('Expert view'), self)
        actionExpertView.setCheckable(True)
        actionExpertView.triggered.connect(self._setExpertView)
        actionExpertView.setChecked(True)
    
        toggleSimpleView    = QActionGroup(self)
        toggleSimpleView.addAction(actionMinimalView)
        toggleSimpleView.addAction(actionSimpleView)
        toggleSimpleView.addAction(actionExpertView)
        toggleSimpleView.setExclusive(True)
    
        menuWin     = menu.addMenu(self.tr('Views'))
        menuWin.addAction(actionMinimalView)
        menuWin.addAction(actionSimpleView)
        menuWin.addAction(actionExpertView)
        menuWin.addSeparator()
        menuWin.addAction(fullScreenAction)
    
        " configure menu "
    
        actionConfigureProxy = QAction(self.tr('Proxy settings'), self)
        actionConfigureProxy.triggered.connect(self._launchProxySettings)
    
        menuConf    = menu.addMenu(self.tr('Configure'))
        menuConf.addAction(actionConfigureProxy)
    
        " style menu "
        nativeAction    = QAction(self.tr('Native'), self)
        nativeAction.setCheckable(True)
        nativeAction.triggered.connect(partial(self._setStyle, 'Native'))
    
        plastiqueAction = QAction(self.tr('plastique'), self)
        plastiqueAction.setCheckable(True)
        plastiqueAction.triggered.connect(partial(self._setStyle, 'Plastique'))
    
        cleanlooksAction = QAction(self.tr('cleanlooks'), self)
        cleanlooksAction.setCheckable(True)
        cleanlooksAction.triggered.connect(partial(self._setStyle, 'Cleanlooks'))
    
        cdeAction       = QAction(self.tr('cde'), self)
        cdeAction.setCheckable(True)
        cdeAction.triggered.connect(partial(self._setStyle, 'CDE'))
    
        motifAction     = QAction(self.tr('motif'), self)
        motifAction.setCheckable(True)
        motifAction.triggered.connect(partial(self._setStyle, 'Motif'))
    
        windowAction    = QAction(self.tr('windows classic'), self)
        windowAction.setCheckable(True)
        windowAction.triggered.connect(partial(self._setStyle, 'Windows'))
    
        windowxpAction  = QAction(self.tr('windows xp'), self)
        windowxpAction.setCheckable(True)
        windowxpAction.triggered.connect(partial(self._setStyle, 'WindowXP'))
    
        styleToggle = QActionGroup(self)
        styleToggle.addAction(plastiqueAction)
        styleToggle.addAction(cleanlooksAction)
        styleToggle.addAction(nativeAction)
        styleToggle.addAction(cdeAction)
        styleToggle.addAction(motifAction)
        styleToggle.addAction(windowAction)
        styleToggle.addAction(windowxpAction)
        styleToggle.setExclusive(True)
    
        print "style is ", self._noctopusStyle
        if self._noctopusStyle == 'Native':
            nativeAction.setChecked(True)
        elif self._noctopusStyle == 'Plastique':
            plastiqueAction.setChecked(True)
        elif self._noctopusStyle == 'Cleanlooks':
            cleanlooksAction.setChecked(True)
        elif self._noctopusStyle == 'CDE':
            cdeAction.setChecked(True)
        elif self._noctopusStyle == 'Motif':
            motifAction.setChecked(True)
        elif self._noctopusStyle == 'Windows':
            windowAction.setChecked(True)
        elif self._noctopusStyle == 'WindowXP':
            windowxpAction.setChecked(True)
        else:
            plastiqueAction.setChecked(True)
    
        menuStyle = menu.addMenu(self.tr('Style'))
        menuStyle.addAction(nativeAction)
        menuStyle.addAction(plastiqueAction)
        menuStyle.addAction(cleanlooksAction)
        menuStyle.addAction(cdeAction)
        menuStyle.addAction(motifAction)
        menuStyle.addAction(windowAction)
        menuStyle.addAction(windowxpAction)
    
        return
