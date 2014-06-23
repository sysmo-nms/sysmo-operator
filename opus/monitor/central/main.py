from    noctopus_widgets    import (
    NFrameContainer, NFrame,
    NGridContainer, NGrid
)

from    opus.monitor.central.tree.main          import ProbesTree
from    opus.monitor.central.timeline.main      import Timeline

class TreeContainer(NFrameContainer):
    
    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self._probesTree = ProbesTree(self)
        self._timeline   = Timeline(self)
        self._grid = NGridContainer(self)
        self._grid.setVerticalSpacing(6)
        self._grid.addWidget(self._probesTree,         1, 0)
        self._grid.addWidget(self._timeline,           2, 0)

        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,2)
        self._grid.setRowStretch(2,1)
        self.setLayout(self._grid)
