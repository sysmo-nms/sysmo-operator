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
        #self._timeline   = Timeline(self)
        self._grid = NGridContainer(self)
        self._grid.setVerticalSpacing(6)

        self._grid.addWidget(self._splitter, 1, 0)
        #self._grid.addWidget(self._timeline, 2, 0)

        self._grid.setRowStretch(1,1)
        #self._grid.setRowStretch(2,0)
        self.setLayout(self._grid)

class MainSplitter(QSplitter):
    def __init__(self, parent):
        super(MainSplitter, self).__init__(parent)
        sysmapi.nConnectAppToggled(self._toggle)
        sysmapi.nConnectWillClose(self._saveSettings)
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
        settings = QSettings()
        state  = settings.value('monitor/main_splitter')
        mapvis = settings.value('monitor/main_splitter_map')
        geom   = settings.value('monitor/main_splitter_geo')

        if state is not None: self.restoreState(state)

        if geom  is not None: self.restoreGeometry(geom)
        if mapvis == 'false':
            self._maps.hide()
    
    def _saveSettings(self):
        settings = QSettings()
        settings.setValue('monitor/main_splitter', self.saveState())
        settings.setValue('monitor/main_splitter_geo', self.saveGeometry())
        settings.setValue('monitor/main_splitter_map', self._maps.isVisible())
