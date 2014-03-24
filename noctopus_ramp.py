# python lib
from functools import partial

# PySide
from    PySide.QtCore   import (
    Qt,
    Signal,
    QSettings,
    QSize
)

from    PySide.QtGui    import (
    QAction,
    QActionGroup,
    QSizePolicy,
    QPushButton,
    QButtonGroup,
    QMenu,
    QLabel,
    QToolButton,
)


# local dependencies
from    noctopus_images     import getIcon
from    noctopus_widgets    import NFrameContainer, NGridContainer, NFrame

# extentions
import  opus.monitor.main
import  opus.locator.main
import  opus.logviewer.main
import  opus.iphelper.main
import  opus.scheduller.main
import  opus.knowledge.main


# SELECTOR RAMP ###############################################################
class NSelector(NFrameContainer):
    
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

        self._restoreSettings()
        self._initGrid()
        self._updateGrid()

    def _initGrid(self):
        self.grid = NGridContainer(self)
        self.grid.setVerticalSpacing(2)
        self.grid.addWidget(self.menuButton, 0,0)
        self.setLayout(self.grid)

    def _updateGrid(self):
        for key in self._buttons.keys():
            self.grid.addWidget(
                self._buttons[key]['widget'],
                self._buttons[key]['row'],
                0)
            self.grid.setRowStretch(self._buttons[key]['row'], 1)

        self.currentView = 'monitor'
        self.setLayout(self.grid)

    def _restoreSettings(self):
        self.currentView = 'monitor'

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
        self._buttons['monitor']['widget'] = NSelectorButton(self, 'monitor')
        self._buttons['monitor']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['locator'] = dict()
        self._buttons['locator']['row'] = 2
        self._buttons['locator']['widget'] = NSelectorButton(self, 'locator')
        self._buttons['locator']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['logviewer'] = dict()
        self._buttons['logviewer']['row'] = 3
        self._buttons['logviewer']['widget'] = NSelectorButton(self, 'logviewer')
        self._buttons['logviewer']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['iphelper'] = dict()
        self._buttons['iphelper']['row'] = 4
        self._buttons['iphelper']['widget'] = NSelectorButton(self, 'iphelper')
        self._buttons['iphelper']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['scheduller'] = dict()
        self._buttons['scheduller']['row'] = 5
        self._buttons['scheduller']['widget'] = NSelectorButton(self, 'scheduller')
        self._buttons['scheduller']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

        self._buttons['knowledge'] = dict()
        self._buttons['knowledge']['row'] = 6
        self._buttons['knowledge']['widget']  = NSelectorButton(self, 'knowledge')
        self._buttons['knowledge']['widget'].setIcon(
            getIcon('utilities-system-monitor-black'))

    def _initStack(self):
        self.appButtonPressed.connect(self._stackWidget.selectEvent)

        self._stackWidget.addLayer(opus.monitor.main.Central,    'monitor')
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

    def goUp(self, mod):
        print "go up ", mod

    def goDown(self, mod):
        print "go down ", mod

    def goRemove(self, mod):
        print "go remove ", mod




# SELECTOR BUTTON #############################################################
class NSelectorButton(QPushButton):
    def __init__(self, parent, identifier):
        super(NSelectorButton, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(buttonPol)
        self.setIconSize(QSize(30,100))
        self.setCheckable(True)
        self._identifier = identifier
        self._parent     = parent
        self._initMenu()

    def _initMenu(self):
        self._menu = QMenu(self)
        self.goUp    = self._menu.addAction(getIcon('go-up'),       'Move up')
        self.goDown  = self._menu.addAction(getIcon('go-down'),     'Move down')
        self.goRemove = self._menu.addAction(getIcon('list-remove'), 'Remove')

        self.goUp.triggered.connect(partial(self._parent.goUp, self._identifier))
        self.goDown.triggered.connect(partial(self._parent.goDown, self._identifier))
        self.goRemove.triggered.connect(partial(self._parent.goRemove,self._identifier))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._menu.exec_(self.mapToGlobal(event.pos()))
        QPushButton.mousePressEvent(self, event)

    def isTop(self):
        self.goUp.isDisabled(True)

    def isDown(self):
        self.goDown.isDisabled(True)

    def noTopNoDown(self):
        self.goUp.isDisabled(False)
        self.goDown.isDisabled(False)
