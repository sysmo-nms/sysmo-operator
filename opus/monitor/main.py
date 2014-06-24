from    PySide.QtCore   import (
    QSettings,
    QTimeLine
)

from    opus.monitor                 import norrd
from    opus.monitor.commands.user_actions import UserActions
from    opus.monitor.central.main    import TreeContainer
from    opus.monitor.proxy           import ChanHandler
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
        #nocapi.nConnectAppToggled(self._toggleStack)

        self._initRrdtool()
        self._initChanProxy()
        self._initUserActions()

        grid  = NGridContainer(self)
        grid.addWidget(TreeContainer(self))
        self.setLayout(grid)
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

    def _initRrdtool(self):
        self._rrdtool = norrd.Rrdtool(self)
        nocapi.nConnectWillClose(self._rrdtool.threadShutdown)


    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _willClose(self): pass
