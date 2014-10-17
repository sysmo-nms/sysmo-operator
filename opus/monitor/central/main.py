from PySide.QtGui import QSplitter, QStackedWidget
from PySide.QtCore import QSettings, QTimeLine
from    noctopus_widgets    import (
    NFrameContainer, NFrame,
    NGridContainer, NGrid
)

from    opus.monitor.central.tree.main          import ProbesTree
from    opus.monitor.central.timeline.main      import Timeline
from    opus.monitor.central.osmap.main         import OSMapContainer
#import  opus.monitor.api as monapi
import  nocapi

class TreeContainer(NFrameContainer):
    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self._treeStack  = TreeStack(self)
        self._timeline   = Timeline(self)
        self._grid = NGridContainer(self)
        self._grid.setVerticalSpacing(6)

        self._grid.addWidget(self._treeStack,          1, 0)
        self._grid.addWidget(self._timeline,           2, 0)

        self._grid.setRowStretch(1,1)
        self._grid.setRowStretch(2,0)
        self.setLayout(self._grid)

class TreeStack(QStackedWidget):
    def __init__(self, parent):
        super(TreeStack, self).__init__(parent)
        nocapi.nConnectAppToggled(self._toggleSplitter)
        self._osmap = OSMapContainer(self)
        self._ptree = ProbesTree(self)
        self.addWidget(self._ptree)
        self.addWidget(self._osmap)

    def _toggleSplitter(self, msg):
        if msg['id']        != 'monitor': return
        if msg['button']    != 'left': return
        if (self.currentWidget() == self._ptree):
            self.setCurrentWidget(self._osmap)
        else:
            self.setCurrentWidget(self._ptree)
