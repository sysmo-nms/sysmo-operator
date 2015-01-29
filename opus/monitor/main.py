from    PyQt5.QtCore   import (
    QSettings,
    QTimeLine,
)

from PyQt5.QtGui import QMenu, QAction
# TOPYQT ERROR BEGIN
# AttributeError: 'module' object has no attribute 'STARTF_USESHOWWINDOW
#from    opus.monitor                 import norrd
# TOPYQT ERROR END
from    opus.monitor.commands.user_actions  import UserActions
from    opus.monitor.commands.doc_engine    import DocConfigurator
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
        wikiConf = QAction('Configure documentation engine...', self)
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

    # TOPYQT ERROR BEGIN
    # AttributeError: 'module' object has no attribute 'STARTF_USESHOWWINDOW
    def _initRrdtool(self): pass
        #norrd.start(self)
        #nocapi.nConnectWillClose(norrd.stop)
    # TOPYQT ERROR END

    def _configureDoc(self):
        ret = DocConfigurator(self)

    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _willClose(self): pass
