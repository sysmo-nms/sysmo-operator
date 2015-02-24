from    PyQt5.QtGui   import QIcon
from    PyQt5.QtCore   import (
    QSettings,
    QTimeLine,
)

from PyQt5.QtWidgets import QMenu, QAction
from    monitor                 import norrd
from    monitor.commands.user_actions  import UserActions
from    monitor.commands.doc_engine    import DocConfigurator
from    monitor.central.main    import TreeContainer
from    monitor.proxy           import ChanHandler
from    sysmo_widgets             import (
    NFrameContainer,
    NGridContainer
)

import  sysmapi

class Central(NFrameContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        Central.singleton = self
        sysmapi.nConnectWillClose(self._willClose)
        menu = QMenu('monitor', self)
        menu.setIcon(QIcon(sysmapi.nGetPixmap('utilities-system-monitor')))
        wikiConf = QAction('Configure documentation engine...', self)
        wikiConf.setIcon(QIcon(sysmapi.nGetPixmap('folder-saved-search')))
        wikiConf.triggered.connect(self._configureDoc)
        menu.addAction(wikiConf)
        sysmapi.nAddMainMenu(menu)

        self._initRrdtool()
        self._initChanProxy()
        self._initUserActions()

        grid  = NGridContainer(self)
        grid.addWidget(TreeContainer(self))
        self.setLayout(grid)

    def _initUserActions(self):
        self._userActions = UserActions(self)

    def _initRrdtool(self):
        norrd.start(self)
        sysmapi.nConnectWillClose(norrd.stop)

    def _configureDoc(self):
        ret = DocConfigurator(self)

    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _willClose(self): pass
