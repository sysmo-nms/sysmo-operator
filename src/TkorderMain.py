#!/usr/bin/env python
import  time
import  os
import  sys
import  pprint

from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    PySide.QtNetwork    import *
from    TkorderIcons        import TkorderIcons,TkorderImages
import  Supercast
import  ModTracker

_fromUtf8 = lambda s: s

class TkorderClient(QMainWindow):
    " The main tkorder window "
    def __init__(self, parent=None):
        super(TkorderClient, self).__init__(parent)
        TkorderIcons.init()
        TkorderImages.init()
        TkorderClient.singleton = self

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
        #self.statusBar.setStyleSheet(
        #    "QStatusBar { \
        #        border: 1px solid black;\
        #        border-radius: 50px;\
        #        background: #B0C2D9 \
        #    }")
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
        menuWin     = menu.addMenu('Views')
        menuWin.addAction(fullScreenAction)


        " Server connexion and socket related "
        self.supercast = Supercast.Link(self)
        self.supercast.setSocketServer('localhost')
        self.supercast.setSocketPort(8888)

        " End init "
        self.setCentralWidget(
            TkorderCentralWidget(self))
        self.updateStatusBar("Started!")

    def toggleFullScreen(self):
        if self.isFullScreen() == False:
            self.showFullScreen()
        else:
            self.showNormal()
        
    def logTargets(self):
        pp  = pprint.PrettyPrinter(indent=4)
        d   = ModTracker.TrackerMain.singleton.targets
        print pp.pprint(d)

    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)

    def getSettings(self):
        return self.config

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
        self.mod1 = RotatedButton(self, 'Monitor', 'est')
        self.mod2 = RotatedButton(self, 'Manage',  'est')
        mod1Pol = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mod2Pol = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mod1.setSizePolicy(mod1Pol)
        self.mod1.setCheckable(True)
        self.mod1.setIcon(TkorderIcons.get('utilities-system-monitor'))
        self.mod2.setSizePolicy(mod2Pol)
        self.mod2.setIcon(TkorderIcons.get('emblem-system'))
        grid.addWidget(self.mod1, 0,0)
        grid.addWidget(self.mod2, 1,0)
        self.setLayout(grid)

    def connectAll(self):
        self.mod1.clicked.connect(ModTracker.TrackerMain.singleton.leftClicked)

class RotatedButton(QPushButton):
    # XXX rotate the icon but dit not print the text 
    def __init__(self, text, parent, orientation = "west"):
        super(RotatedButton,self).__init__(text, parent)
        self.orientation = orientation

    def paintEvent(self, event):
        painter = QStylePainter(self)
        painter.rotate(90)
        painter.translate(0, -1 * self.width());
        painter.drawControl(QStyle.CE_PushButton, self.getSyleOptions())

    def minimumSizeHint(self):
        size = super(RotatedButton, self).minimumSizeHint()
        size.transpose()
        return size

    def sizeHint(self):
        size = super(RotatedButton, self).sizeHint()
        size.transpose()
        return size

    def getSyleOptions(self):
        options = QStyleOptionButton()
        options.initFrom(self)
        size = options.rect.size()
        size.transpose()
        options.rect.setSize(size)
        options.features = QStyleOptionButton.None
        if self.isFlat():
            options.features |= QStyleOptionButton.Flat
        if self.menu():
            options.features |= QStyleOptionButton.HasMenu
        if self.autoDefault() or self.isDefault():
            options.features |= QStyleOptionButton.AutoDefaultButton
        if self.isDefault():
            options.features |= QStyleOptionButton.DefaultButton
        if self.isDown() or (self.menu() and self.menu().isVisible()):
            options.state |= QStyle.State_Sunken
        if self.isChecked():
            options.state |= QStyle.State_On
        if not self.isFlat() and not self.isDown():
            options.state |= QStyle.State_Raised

        options.text = self.text()
        options.icon = self.icon()
        options.iconSize = self.iconSize()
        return options

class ModView(QFrame):
    def __init__(self, parent):
        super(ModView, self).__init__(parent)
        grid        = QGridLayout(self)
        grid.setContentsMargins(5,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        modTracker  = ModTracker.TrackerMain(self)
        grid.addWidget(modTracker, 0, 0)
        self.setLayout(grid)

def main(arguments):
    tkorderApp    = QApplication(arguments)
    #fo = open('style/dib.stylesheet')
    #styleSheet = fo.read()
    #fo.close()
    #tkorderApp.setStyleSheet(styleSheet)
    tkorderUi     = TkorderClient()
    tkorderApp.setWindowIcon(
        TkorderIcons.get('applications-development')
    )

    #print QStyleFactory.keys()
    #tkorderApp.setStyle('Plastique')
    loginUi         = Supercast.LogInDialog2()
    loginUi.supercastClient = tkorderUi
    loginUi.show()

    sys.exit(tkorderApp.exec_())
