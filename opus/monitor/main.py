from    PySide.QtCore   import (
    QSettings,
    QTimeLine,
)

from PySide.QtGui import QMenu, QAction
from    opus.monitor                 import norrd
from    opus.monitor.commands.user_actions import UserActions
from    opus.monitor.commands.doc_conf      import DocConfigurator
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
        menu = QMenu('monitor', self)
        menu.setIcon(nocapi.nGetIcon('utilities-system-monitor'))
        wikiConf = QAction('Configure documentation engine', self)
        wikiConf.setIcon(nocapi.nGetIcon('folder-saved-search'))
        wikiConf.triggered.connect(self._configureDoc)
        menu.addAction(wikiConf)
        nocapi.nAddMainMenu(menu)

        self._initRrdtool()
        self._initChanProxy()
        self._initUserActions()

        grid  = NGridContainer(self)
        grid.addWidget(TreeContainer(self))
        self.setLayout(grid)

    def _initUserActions(self):
        self._userActions = UserActions(self)

    def _initRrdtool(self):
        self._rrdtool = norrd.Rrdtool(self)
        nocapi.nConnectWillClose(self._rrdtool.threadShutdown)

    def _configureDoc(self):
        ret = DocConfigurator(self)
        print 'configure wiki url ', ret


    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _willClose(self): pass
