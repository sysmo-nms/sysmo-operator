# python lib
from functools import partial

# PyQt4
from    PyQt4.QtNetwork import QAbstractSocket
from    PyQt4.QtCore   import (
    Qt,
    pyqtSignal,
    QSettings,
    QSize,
    QObject
)

from    PyQt4.QtGui    import (
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
    QMessageBox,
    QWidgetAction
)


# local dependencies
from    noctopus_colors     import getPalette
from    noctopus_images     import getIcon, noctopusGraphicsInit, dumpPalette
from    noctopus_dialogs    import Proxy
from    noctopus_statusbar  import NStatusBar
from    noctopus_centerwidget   import NCentralFrame
from    noctopus_widgets    import Community

# supercast
from  supercast.main    import Supercast


class NMainWindow(QMainWindow):

    " The noctopus QMainWindow "

    proxySettings   = pyqtSignal(dict)
    # emit self.activeProxySettings dict: {
    #   'use':  True | False,
    #   'host': str,
    #   'port': int
    # }

    viewMode        = pyqtSignal(dict)
    # emit self.activeViewMode dict: {
    #   'screen':   'full' | 'normal',
    #   'mode':     'minimal' | 'simple' | 'expert',
    #   'tray':     'traymin' | 'traymax'
    # }

    willClose       = pyqtSignal()
    # emit when the application will close

    supercastEnabled = pyqtSignal()
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
        self._initMenus()
        self._initLayout()


    #########
    # INITS #
    #########

    # Supercast
    def _initSupercast(self):
        self.supercastLogged = False
        self.supercast = Supercast(self, mainwindow=self)
        self.supercast.eventpyqtSignals.connect(self._handleSupercastEvents)
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
        #settings = QSettings("Noctopus NMS", "noctopus-client")
        settings    = QSettings()
        settings.setValue("NMainWindow/geometry",       self.saveGeometry())
        settings.setValue("NMainWindow/windowState",    self.saveState())
        settings.setValue("NMainWindow/proxySettings",  self.activeProxySettings)
        settings.setValue("NMainWindow/viewMode",       self.activeViewMode)
        settings.setValue("NMainWindow/style",          self._noctopusStyle)
        settings.setValue("NMainWindow/theme",          self._noctopusTheme)
        self.supercast.supercastClose()
        QMainWindow.closeEvent(self, event)

    ############
    # SETTINGS #
    ############
    def _restoreSettings(self):
        #settings = QSettings("Noctopus NMS", "noctopus-client")
        settings = QSettings()

        self.restoreGeometry(settings.value("NMainWindow/geometry"))
        self.restoreState(settings.value("NMainWindow/windowState"))

        proxySet = settings.value("NMainWindow/proxySettings")
        if proxySet != None: self.activeProxySettings = proxySet

        self._noctopusTheme = settings.value("NMainWindow/theme")
        self._noctopusStyle = settings.value("NMainWindow/style")

        #viewMode = settings.value("NMainWindow/viewMode")
        #if viewMode != None: self.activeViewMode = viewMode
        #activeOpus = ...

    #####################
    # STYLES AND THEMES #
    #####################
    def _setStyle(self, style):
        self._noctopusStyle = style
        if style == 'native':   self.menuColor.setDisabled(True)
        else:                   self.menuColor.setDisabled(False)
        self._needRestart()

    def _setTheme(self, theme):
        self._noctopusTheme = theme
        self._needRestart()

    def _needRestart(self):
        msgBox = QMessageBox(self)
        msgBox.setText(self.tr('The application must restart to take your modification in consideration'))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    #########
    # MENUS #
    #########
    def _communityPressed(self):
        print "community pressed ajouter soumettre bug ou soumettre idee"

    def _initMenus(self):
        " Menu bar "
        menu = self.menuBar()
        menu.setAutoFillBackground(True)

        "top corner widget"
        communityButton = QPushButton(self)
        communityButton.setLayoutDirection(Qt.RightToLeft)
        communityButton.setContentsMargins(0,0,0,0)
        communityButton.setIcon(getIcon('system-users'))
        communityButton.setFlat(True)
        communityAction = QWidgetAction(self)
        communityAction.setDefaultWidget(Community(self))
        communityMenu   = QMenu(self)
        communityMenu.addAction(communityAction)
        communityButton.setMenu(communityMenu)
        menu.setCornerWidget(communityButton)

        "File"
        menuFile    = menu.addMenu('Noctopus')
        _dumpPaletteAction = QAction('dump palette', self)
        _dumpPaletteAction.triggered.connect(self._dumpPalette)

        exitAction      = QAction(getIcon('system-log-out'), self.tr('&Exit'), self)
        updateAction    = QAction(
            getIcon('software-update-available'),
            self.tr('Check for update'),
            self
        )
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        actionConfigureProxy = QAction(self.tr('Proxy settings...'), self)
        actionConfigureProxy.triggered.connect(self._launchProxySettings)
        menuFile.addAction(_dumpPaletteAction)
        menuFile.addAction(updateAction)
        menuFile.addAction(actionConfigureProxy)
        menuFile.addSeparator()
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
    
    
        " style menu "
        nativeAction    = QAction(self.tr('Native'), self)
        nativeAction.setCheckable(True)
        nativeAction.triggered.connect(partial(self._setStyle, 'native'))
    
        plastiqueAction = QAction(self.tr('Balanced'), self)
        plastiqueAction.setCheckable(True)
        plastiqueAction.triggered.connect(partial(self._setStyle, 'plastique'))

        cdeAction = QAction(self.tr('CDE'), self)
        cdeAction.setCheckable(True)
        cdeAction.triggered.connect(partial(self._setStyle, 'cde'))

    
        styleToggle = QActionGroup(self)
        styleToggle.addAction(plastiqueAction)
        styleToggle.addAction(cdeAction)
        styleToggle.addAction(nativeAction)
        styleToggle.setExclusive(True)
    
        menuStyle = menu.addMenu(self.tr('Style'))
        menuStyle.addAction(nativeAction)
        menuStyle.addSeparator()
        menuStyle.addAction(plastiqueAction)
        menuStyle.addAction(cdeAction)

        "color sub menu"
        self.menuColor = menuStyle.addMenu(getIcon('preferences-desktop-theme'),self.tr('Colors'))
        nativeThemeAction = QAction(self.tr('Native'), self)
        nativeThemeAction.setCheckable(True)
        nativeThemeAction.triggered.connect(partial(self._setTheme, 'native'))

        deepWaterAction = QAction(self.tr('Dark'), self)
        deepWaterAction.setCheckable(True)
        deepWaterAction.triggered.connect(partial(self._setTheme, 'dark'))
    
        islandAction = QAction(self.tr('Inland'), self)
        islandAction.setCheckable(True)
        islandAction.triggered.connect(partial(self._setTheme, 'terra'))

        lagoonAction = QAction(self.tr('Lagoon'), self)
        lagoonAction.setCheckable(True)
        lagoonAction.triggered.connect(partial(self._setTheme, 'lagoon'))

        kritaAction = QAction(self.tr('Greys'), self)
        kritaAction.setCheckable(True)
        kritaAction.triggered.connect(partial(self._setTheme, 'krita'))

        desertAction = QAction(self.tr('Desert'), self)
        desertAction.setCheckable(True)
        desertAction.triggered.connect(partial(self._setTheme, 'desert'))

        honeyAction = QAction(self.tr('Honey'), self)
        honeyAction.setCheckable(True)
        honeyAction.triggered.connect(partial(self._setTheme, 'honey'))

        snowAction = QAction(self.tr('Snow'), self)
        snowAction.setCheckable(True)
        snowAction.triggered.connect(partial(self._setTheme, 'snow'))

        groupColor = QActionGroup(self)
        groupColor.addAction(nativeThemeAction)
        groupColor.addAction(deepWaterAction)
        groupColor.addAction(lagoonAction)
        groupColor.addAction(islandAction)
        groupColor.addAction(kritaAction)
        groupColor.addAction(desertAction)
        groupColor.addAction(honeyAction)
        groupColor.addAction(snowAction)
        groupColor.setExclusive(True)

        if self._noctopusTheme == 'lagoon':
            lagoonAction.setChecked(True)
        elif self._noctopusTheme == 'dark':
            deepWaterAction.setChecked(True)
        elif self._noctopusTheme == 'terra':
            islandAction.setChecked(True)
        elif self._noctopusTheme == 'krita':
            kritaAction.setChecked(True)
        elif self._noctopusTheme == 'desert':
            desertAction.setChecked(True)
        elif self._noctopusTheme == 'honey':
            honeyAction.setChecked(True)
        elif self._noctopusTheme == 'snow':
            snowAction.setChecked(True)
        else:
            nativeThemeAction.setChecked(True)

        self.menuColor.addAction(nativeThemeAction)
        self.menuColor.addSeparator()
        self.menuColor.addAction(deepWaterAction)
        self.menuColor.addAction(islandAction)
        self.menuColor.addAction(lagoonAction)
        self.menuColor.addAction(kritaAction)
        self.menuColor.addAction(desertAction)
        self.menuColor.addAction(honeyAction)
        self.menuColor.addAction(snowAction)

        if self._noctopusStyle == 'native':
            nativeAction.setChecked(True)
            self.menuColor.setDisabled(True)
        elif self._noctopusStyle == 'plastique':
            plastiqueAction.setChecked(True)
        elif self._noctopusStyle == 'cde':
            cdeAction.setChecked(True)
        else:
            nativeAction.setChecked(True)

        " application menu defined by the differents extentions"
        menu.addSeparator()

        self._mainMenu = menu
        return

    def setApplicationMenu(self, menu):
        self._mainMenu.addMenu(menu)

    def _dumpPalette(self):
        dumpPalette()
