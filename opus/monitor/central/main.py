from PySide.QtGui import QSplitter, QStackedWidget
from PySide.QtCore import QSettings, QTimeLine
from    noctopus_widgets    import (
    NFrameContainer, NFrame,
    NGridContainer, NGrid
)

from    opus.monitor.central.tree.main          import ProbesTree
from    opus.monitor.central.timeline.main      import Timeline
from    opus.monitor.central.rightmaps.main         import RightMapsContainer
#import  opus.monitor.api as monapi
import  nocapi

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
        self._maps  = RightMapsContainer(self)
        self._ptree = ProbesTree(self)
        self.insertWidget(0,self._ptree)
        self.insertWidget(1,self._maps)
        self.setStretchFactor(0,0)
        self.setStretchFactor(1,1)
        self.setCollapsible(0,False)
        self.setCollapsible(1,False)

        self._loadSettings()

    def _loadSettings(self):
        nocapi.nConnectWillClose(self._saveSettings)
        self._settings = QSettings()
        state = self._settings.value('monitor/main_splitter')
        if state == None: return
        self.restoreState(state)

    def _saveSettings(self):
        self._settings.setValue('monitor/main_splitter', self.saveState())
