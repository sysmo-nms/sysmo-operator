from    PyQt5.QtGui import QIcon
from    PyQt5.QtWidgets import QMenu, QAction
from    monitor import norrd
from    monitor.user_operations import UserOperations
from    monitor.dialogs.doc_engine import DocConfigurator
from    monitor.gui.main import TreeContainer
from    monitor.proxy import ChanHandler
from    sysmo_widgets import NFrameContainer, NGridContainer
import  sysmapi

class Central(NFrameContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        Central.singleton = self
        sysmapi.nConnectWillClose(self._willClose)
        menu = QMenu('Monitor', self)
        wikiConf = QAction('Configure documentation engine...', self)
        wikiConf.setIcon(QIcon(sysmapi.nGetPixmap('folder-saved-search')))
        wikiConf.triggered.connect(self._configureDoc)
        menu.addAction(wikiConf)
        sysmapi.nAddMainMenu(menu)

        self._initRrdtool()
        self._initChanProxy()
        self._initUserOperations()

        grid  = NGridContainer(self)
        grid.addWidget(TreeContainer(self))
        self.setLayout(grid)

    def _initUserOperations(self):
        self._userOperations = UserOperations(self)

    def _initRrdtool(self):
        norrd.start(self)
        sysmapi.nConnectWillClose(norrd.stop)

    def _configureDoc(self):
        ret = DocConfigurator(self)

    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _willClose(self): pass
