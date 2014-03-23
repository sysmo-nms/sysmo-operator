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
    QMessageBox
)


# local dependencies
from    noctopus_images     import getIcon, noctopusGraphicsInit
from    noctopus_dialogs    import Proxy
from    noctopus_statusbar  import NStatusBar
from    noctopus_centerwidget   import NCentralFrame
from    noctopus_menus      import initMenus

# supercast
from  supercast.main    import Supercast

# extentions
#import  Monitor.main
#import  opus.locator.main
#import  opus.logviewer.main
#import  opus.iphelper.main
#import  opus.scheduller.main
#import  opus.knowledge.main


##############################################################################
####################### MAIN WINDOW ##########################################
##############################################################################
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


    #########
    # INITS #
    #########

    # Supercast
    def _initSupercast(self):
        self._supercastLogged = False
        self._supercast = Supercast(self, mainwindow=self)
        self._supercast.eventSignals.connect(self._handleSupercastEvents)
        self._supercast.tryLogin()

    def _handleSupercastEvents(self, event):
        (key, payload) = event
        if    key == 'success':
            self._supercastLogged = True
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
    def _initMenus(self):
        initMenus(self)

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
        msgBox.setText('The application must restart to take your modification in consideration')
        msgBox.setInformativeText('Do you want to restart it now?')
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        if msgBox.exec_() == QMessageBox.Yes:  self.close()

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
        if proxySet != None: self.activeProxySettings = proxySet

        noctoStyle = settings.value("NMainWindow/style")
        if noctoStyle != None: self._noctopusStyle = noctoStyle

        #viewMode = settings.value("NMainWindow/viewMode")
        #if viewMode != None: self.activeViewMode = viewMode
        #activeOpus = ...
