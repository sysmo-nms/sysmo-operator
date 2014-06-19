from    PySide.QtCore   import (
    QSettings,
    QTimeLine
)

from    PySide.QtGui   import (
    QStackedWidget
)

from    opus.monitor                 import norrd
from    opus.monitor.commands.user_actions import UserActions
from    opus.monitor.trees_area.main import TreeContainer
from    opus.monitor.proxy           import ChanHandler
from    opus.monitor.widgets         import OSMView
from    noctopus_widgets             import (
    NFrameContainer,
    NGridContainer
)

import  nocapi

class Central(NFrameContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        Central.singleton = self
        nocapi.nConnectWillClose(self._willClose)
        nocapi.nConnectAppToggled(self._toggleStack)

        self._initRrdtool()
        self._initChanProxy()
        self._initUserActions()

        self._initLayout()
        self._initDockWidget()

    def _toggleStack(self, msg):
        if msg['id']        != 'monitor': return
        if msg['button']    != 'left': return

        if self._stack.currentIndex() == 1:
            self._stack.setCurrentIndex(0)
        else:
            self._stack.setCurrentIndex(1)

    def _initUserActions(self):
        self._userActions = UserActions(self)

    def _initDockWidget(self): pass
#         tko.addTopDockWidget(Summary(self), 'Monitori')

    def _initLayout(self):
        self._stack = QStackedWidget(self)
        self._stack.insertWidget(0, TreeContainer(self))
        self._stack.insertWidget(1, OSMView(self))

        grid  = NGridContainer(self)
        grid.addWidget(self._stack)
        self.setLayout(grid)

    def _initRrdtool(self):
        self._rrdtool = norrd.Rrdtool(self)
        nocapi.nConnectWillClose(self._rrdtool.threadShutdown)


    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _willClose(self): pass
