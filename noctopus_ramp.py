# python lib
from functools import partial

# PyQt4
from    PyQt4.QtCore   import (
    Qt,
    pyqtSignal,
    QSettings,
    QSize
)

from    PyQt4.QtGui    import (
    QAction,
    QActionGroup,
    QSizePolicy,
    QPushButton,
    QButtonGroup,
    QMenu,
    QLabel,
    QToolButton,
)

from PyQt4.QtSvg   import QSvgWidget

# local dependencies
from    noctopus_images     import getIcon, getImage
from    noctopus_widgets    import NFrameContainer, NGridContainer, NFrame, NGrid

# opus
import  opus.monitor.main
import  opus.dashboard.main
#import  opus.netman.main
#import  opus.knowledge.main
#import  opus.schedule.main
#import  opus.tickets.main
#import  opus.metro.main

# SELECTOR RAMP ###############################################################
class NSelector(NFrameContainer):
    
    " left button ramp container "

    appButtonPressed = pyqtSignal(str)
    appButtonToggled = pyqtSignal(dict)

    def __init__(self, parent, stackWidget):
        super(NSelector, self).__init__(parent)
        NSelector.singleton = self
        self.setContentsMargins(0,2,0,2)
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
        self.grid.setVerticalSpacing(4)
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
        self._buttons['monitor']['widget'].setIcon('monitor-black')

        self._buttons['dashboard'] = dict()
        self._buttons['dashboard']['row'] = 2
        self._buttons['dashboard']['widget'] = NSelectorButton(self, 'dashboard')
        self._buttons['dashboard']['widget'].setIcon('dashboard-black')

        #self._buttons['netman'] = dict()
        #self._buttons['netman']['row'] = 3
        #self._buttons['netman']['widget'] = NSelectorButton(self, 'netman')
        #self._buttons['netman']['widget'].setIcon('netman-black')

        #self._buttons['knowledge'] = dict()
        #self._buttons['knowledge']['row'] = 4
        #self._buttons['knowledge']['widget']  = NSelectorButton(self, 'knowledge')
        #self._buttons['knowledge']['widget'].setIcon('knowledge-black')

    def _initStack(self):
        self.appButtonPressed.connect(self._stackWidget.selectEvent)

        self._stackWidget.addLayer(opus.monitor.main.Central,    'monitor')
        self._stackWidget.addLayer(opus.dashboard.main.Central,  'dashboard')
        #self._stackWidget.addLayer(opus.netman.main.Central,      'netman')
        #self._stackWidget.addLayer(opus.knowledge.main.Central,  'knowledge')
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
            but.toggle.connect(self._appButtonPressed)
            
    def _appButtonPressed(self, arg):
        identifier = arg['id']
        if self.currentView == identifier:
            self.appButtonToggled.emit(arg)
        else:
            self.appButtonPressed.emit(identifier)
            self.currentView = identifier

    def goUp(self, mod):
        print "go up ", mod

    def goDown(self, mod):
        print "go down ", mod

    def goRemove(self, mod):
        print "go remove ", mod




# SELECTOR BUTTON #############################################################
class NSelectorButton(QPushButton):
    toggle = pyqtSignal(dict)
    def __init__(self, parent, identifier):
        super(NSelectorButton, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setSizePolicy(buttonPol)
        self.setIconSize(QSize(30,100))
        self.setCheckable(True)
        self._identifier = identifier
        self._parent     = parent
        self._initMenu()

    def setIcon(self, image):
        grid = NGrid(self)
        icon = QSvgWidget(getImage(image), self)
        renderer = icon.renderer()
        size = renderer.defaultSize()
        icon.setFixedWidth(size.width() / 2)
        icon.setFixedHeight(size.height() / 2)
        grid.addWidget(icon, 0,0)
        grid.setAlignment(icon, Qt.AlignHCenter)
        grid.setAlignment(icon, Qt.AlignBottom)

    def _initMenu(self):
        self._menu = QMenu(self)
        self.goUp    = self._menu.addAction(getIcon('go-up'),       self.tr('Move up'))
        self.goDown  = self._menu.addAction(getIcon('go-down'),     self.tr('Move down'))
        self.goRemove = self._menu.addAction(getIcon('list-remove'), self.tr('Remove'))

        self.goUp.triggered.connect(partial(self._parent.goUp, self._identifier))
        self.goDown.triggered.connect(partial(self._parent.goDown, self._identifier))
        self.goRemove.triggered.connect(partial(self._parent.goRemove,self._identifier))
    
    # TODO
    def mousePressEvent(self, event):
        bdict = dict()
        if event.button() == Qt.RightButton:
            bdict['id']     = self._identifier
            bdict['button'] = 'right'
            self.toggle.emit(bdict)
        elif event.button() == Qt.LeftButton:
            bdict['id']     = self._identifier
            bdict['button'] = 'left'
            self.toggle.emit(bdict)
        QPushButton.mousePressEvent(self, event)

    def isTop(self):
        self.goUp.isDisabled(True)

    def isDown(self):
        self.goDown.isDisabled(True)

    def noTopNoDown(self):
        self.goUp.isDisabled(False)
        self.goDown.isDisabled(False)
