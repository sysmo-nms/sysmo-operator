from PyQt5.QtCore import Qt, pyqtSignal, QSettings, QSize
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QAction, QActionGroup, QPushButton, QButtonGroup, QMenu, QMessageBox, QWidgetAction, QSizePolicy, QStackedLayout, QLabel, QStatusBar
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgWidget
from sysmo_images import sysmoGraphicsInit, dumpPalette, getPixmap, getImage
from sysmo_dialogs import ProxyConf
from sysmo_widgets import NFrameContainer, NFrame, NGridContainer, NGrid, CommunityMenu
from monitor.gui.timeline.main import Timeline

from supercast.main import Supercast
from functools import partial

import monitor.main
import dashboard.main

MONITOR   = 0
DASHBOARD = 1


class NMainWindow(QMainWindow):

    " The sysmo QMainWindow "

    proxySettings   = pyqtSignal(dict)
    # emit self.activeProxySettings dict: {
    #   'use':  True | False,
    #   'host': str,
    #   'port': int
    # }

    willClose       = pyqtSignal()
    # emit when the application will close

    supercastEnabled = pyqtSignal()
    # emit when supercast is enabled

    def __init__(self, style, parent=None):
        super(NMainWindow, self).__init__(parent)
        NMainWindow.singleton   = self
        self._sysmoStyle     = style
        sysmoGraphicsInit()

        self.setObjectName('MainWindow')
        self.setWindowIcon(QIcon(getPixmap('applications-development')))
        self.setWindowTitle('Sysmo')

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
        self.activeViewMode['tray']     = "traymax"

    # Tray
    def _initTray(self):
        self._trayIcon = QSystemTrayIcon(self)
        self._trayIcon.setIcon(QIcon(getPixmap('applications-development')))
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
        else:
            self.showNormal()
            self.activeViewMode['screen'] = 'normal'

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

    ###########
    # DIALOGS #
    ###########
    def _launchProxySettings(self):
        proxyUi = ProxyConf(self._setProxySettings, parent=self)
        
    def _setProxySettings(self, proxySet):
        self.activeProxySettings = proxySet
        self.proxySettings.emit(self.activeProxySettings)


    #############
    # OVERLOADS #
    #############
    def closeEvent(self, event):
        self.willClose.emit()
        settings    = QSettings()
        #settings.setValue("NMainWindow/geometry",       self.saveGeometry())
        settings.setValue("NMainWindow/windowState",    self.saveState())
        settings.setValue("NMainWindow/windowGeo",      self.saveGeometry())
        settings.setValue("NMainWindow/proxySettings",  self.activeProxySettings)
        settings.setValue("NMainWindow/style",          self._sysmoStyle)
        settings.setValue("NMainWindow/theme",          self._sysmoTheme)
        self.supercast.supercastClose()
        QMainWindow.closeEvent(self, event)

    ############
    # SETTINGS #
    ############
    def _restoreSettings(self):
        settings = QSettings()
        theme = settings.value("NMainWindow/theme")
        style = settings.value("NMainWindow/style")

        if theme is not None:
            self._sysmoTheme = theme 
        else:
            self._sysmoTheme = 'native'

        if style is not None:
            self._sysmoStyle = style 
        else:
            self._sysmoStyle = 'native'

        proxySet = settings.value("NMainWindow/proxySettings")

        if proxySet is not None:
            self.activeProxySettings = proxySet

    def show(self):
        settings = QSettings()
        state = settings.value("NMainWindow/windowState")
        geo   = settings.value("NMainWindow/windowGeo")

        if geo is not None:
            self.restoreGeometry(geo)

        if state is not None: 
            self.restoreState(state)

        QMainWindow.show(self)



    #####################
    # STYLES AND THEMES #
    #####################
    def _setTheme(self, theme):
        self._sysmoTheme = theme
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
        print("community pressed ajouter soumettre bug ou soumettre idee")

    def _initMenus(self):
        " Menu bar "
        menu = self.menuBar()
        menu.setAutoFillBackground(True)

        "top corner widget"
        communityButton = QPushButton(self)
        communityButton.setLayoutDirection(Qt.RightToLeft)
        communityButton.setContentsMargins(0,0,0,0)
        communityButton.setIcon(QIcon(getPixmap('system-users')))
        communityButton.setFlat(True)
        communityAction = QWidgetAction(self)
        communityAction.setDefaultWidget(CommunityMenu(self))
        communityMenu   = QMenu(self)
        communityMenu.addAction(communityAction)
        communityButton.setMenu(communityMenu)
        menu.setCornerWidget(communityButton)

        "File"
        menuFile    = menu.addMenu('Sysmo')
        _dumpPaletteAction = QAction('dump palette', self)
        _dumpPaletteAction.triggered.connect(self._dumpPalette)

        exitAction      = QAction(QIcon(getPixmap('system-log-out')), self.tr('&Exit'), self)
        updateAction    = QAction(
            QIcon(getPixmap('software-update-available')),
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
    
        "View menu"
        fullScreenAction  = QAction(
            QIcon(getPixmap('video-display')), self.tr('&Full screen'), self)
        fullScreenAction.setShortcut('Ctrl+F')
        fullScreenAction.triggered.connect(self._toggleFullScreen)
    
        menuStyle = menu.addMenu(self.tr('View'))
        menuStyle.addAction(fullScreenAction)

        "color sub menu"
        self.menuColor = menuStyle.addMenu(QIcon(getPixmap('preferences-desktop-theme')),self.tr('Colors'))
        nativeThemeAction = QAction(self.tr('Native colors'), self)
        nativeThemeAction.setCheckable(True)
        nativeThemeAction.triggered.connect(partial(self._setTheme, 'native'))

        deepWaterAction = QAction(self.tr('Sysmo (default)'), self)
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

        if self._sysmoTheme == 'lagoon':
            lagoonAction.setChecked(True)
        elif self._sysmoTheme == 'dark':
            deepWaterAction.setChecked(True)
        elif self._sysmoTheme == 'terra':
            islandAction.setChecked(True)
        elif self._sysmoTheme == 'krita':
            kritaAction.setChecked(True)
        elif self._sysmoTheme == 'desert':
            desertAction.setChecked(True)
        elif self._sysmoTheme == 'honey':
            honeyAction.setChecked(True)
        elif self._sysmoTheme == 'snow':
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

        " application menu defined by the differents extentions"
        menu.addSeparator()

        self._mainMenu = menu
        return

    def setApplicationMenu(self, menu):
        self._mainMenu.addMenu(menu)

    def _dumpPalette(self):
        dumpPalette()

# central widget
class NCentralFrame(NFrame):

    " central widget container "

    def __init__(self, parent):
        super(NCentralFrame, self).__init__(parent)
        NCentralFrame.singleton = self
        self.grid = NGrid(self)
        self.grid.setHorizontalSpacing(6)
        self.grid.setVerticalSpacing(6)
        self.selector       = NSelector(self)
        self.centralStack   = NCentralStack(self)
        #self.monitorTimeline = Timeline(self)
        self.selector.buttonGroup.buttonClicked[int].connect(self.centralStack.stack.setCurrentIndex)
        self.grid.addWidget(self.selector,       1,0)
        self.grid.addWidget(self.centralStack,   1,1)
        #self.grid.addWidget(self.monitorTimeline, 2,0,1,2)

        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 1)
        self.grid.setRowStretch(0,0)
        self.grid.setRowStretch(1,1)
        self.setLayout(self.grid)

class NCentralStack(NFrameContainer):

    " main stack container "

    def __init__(self, parent):
        super(NCentralStack, self).__init__(parent)
        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0,0,0,0)
        self.stack.insertWidget(MONITOR,   monitor.main.Central(self))
        self.stack.insertWidget(DASHBOARD, dashboard.main.Central(self))

class NSelector(NFrameContainer):

    appButtonPressed = pyqtSignal(str)
    appButtonToggled = pyqtSignal(dict)


    def __init__(self, parent):
        super(NSelector, self).__init__(parent)
        NSelector.singleton = self
        self.setContentsMargins(0,2,0,2)
        self.setFixedWidth(30)
        grid = NGridContainer(self)
        grid.setVerticalSpacing(4)
        buttonMonit = MonitorButton(self)
        buttonDash  = DashboardButton(self)
        buttonDash.hide()
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(buttonMonit, MONITOR)
        self.buttonGroup.addButton(buttonDash,  DASHBOARD)
        self.buttonGroup.buttonClicked[int].connect(self._signalAll)
        buttonMonit.setChecked(True)
        self.currentIndex = MONITOR
        grid.addWidget(buttonMonit, 0,0)
        grid.addWidget(buttonDash,  1,0)

    def _signalAll(self, index):
        if self.currentIndex == index:
            if index == MONITOR:
                self.appButtonToggled.emit({'button': 'left', 'id': 'monitor'})
            elif index == DASHBOARD:
                self.appButtonToggled.emit({'button': 'left', 'id': 'dashboard'})
        else:
            self.currentIndex = index
            if index == MONITOR:
                self.appButtonPressed.emit('monitor')
            elif self.currentIndex == DASHBOARD:
                self.appButtonPressed.emit('dashboard')
                
class MonitorButton(QPushButton):
    toggle = pyqtSignal(dict)
    def __init__(self, parent):
        super(MonitorButton, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(buttonPol)
        self.setIconSize(QSize(30,100))
        self.setCheckable(True)
        grid = NGrid(self)
        icon = QSvgWidget(getImage('monitor-black'), self)
        renderer = icon.renderer()
        size = renderer.defaultSize()
        icon.setFixedWidth(size.width() / 2)
        icon.setFixedHeight(size.height() / 2)
        grid.addWidget(icon, 0,0)
        grid.setAlignment(icon, Qt.AlignHCenter)
        grid.setAlignment(icon, Qt.AlignBottom)

class DashboardButton(QPushButton):
    toggle = pyqtSignal(dict)
    def __init__(self, parent):
        super(DashboardButton, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(buttonPol)
        self.setIconSize(QSize(30,100))
        self.setCheckable(True)
        grid = NGrid(self)
        icon = QSvgWidget(getImage('dashboard-black'), self)
        renderer = icon.renderer()
        size = renderer.defaultSize()
        icon.setFixedWidth(size.width() / 2)
        icon.setFixedHeight(size.height() / 2)
        grid.addWidget(icon, 0,0)
        grid.setAlignment(icon, Qt.AlignHCenter)
        grid.setAlignment(icon, Qt.AlignBottom)


# status bar
class NStatusBar(QStatusBar):
    def __init__(self, parent):
        super(NStatusBar, self).__init__(parent)
        #debugButton = QToolButton(self)
        #debugButton.setIcon(QIcon(getPixmap('applications-development')))
        #self.addPermanentWidget(debugButton)
