from PyQt5.QtWidgets import QSplitter, QStackedWidget
from PyQt5.QtCore import QSettings, QTimeLine
from    sysmo_widgets    import (
    NFrameContainer, NFrame,
    NGridContainer, NGrid
)

from    monitor.central.tree.main          import ProbesTree
from    monitor.central.timeline.main      import Timeline
from    monitor.central.rightmaps.main         import RightMapsContainer
#import  monitor.api as monapi
import  sysmapi

class TreeContainer(NFrameContainer):
    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self._splitter   = MainSplitter(self)
        self._timeline   = Timeline(self)
        self._grid = NGridContainer(self)
        self._grid.setVerticalSpacing(6)

        self._grid.addWidget(self._splitter, 1, 0)
        self._grid.addWidget(self._timeline, 2, 0)

        self._grid.setRowStretch(1,1)
        self._grid.setRowStretch(2,0)
        self.setLayout(self._grid)

class MainSplitter(QSplitter):
    def __init__(self, parent):
        super(MainSplitter, self).__init__(parent)
        sysmapi.nConnectAppToggled(self._toggle)
        self._maps  = RightMapsContainer(self)
        self._ptree = ProbesTree(self)
        self.insertWidget(0,self._ptree)
        self.insertWidget(1,self._maps)
        self.setStretchFactor(0,0)
        self.setStretchFactor(1,1)
        self.setCollapsible(0,False)
        self.setCollapsible(1,False)

        self._loadSettings()

    def _toggle(self, msg):
        if msg['id'] != 'monitor': return
        if self._maps.isVisible() == True:
            self._maps.hide()
        else:
            self._maps.show()

    def _loadSettings(self):
        sysmapi.nConnectWillClose(self._saveSettings)
        self._settings = QSettings()
        state = self._settings.value('monitor/main_splitter')
        if state == None: return
        # TOPYQT ERROR BEGIN
        # TypeError: QSplitter.restoreState(QByteArray): argument 1 has unexpected type 'QVariant'
        #self.restoreState(state)
        # TOPYQT ERROR END

    def _saveSettings(self):
        self._settings.setValue('monitor/main_splitter', self.saveState())
