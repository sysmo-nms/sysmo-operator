from    noctopus_widgets    import (
    NFrameContainer, NFrame,
    NGridContainer, NGrid
)

from    opus.monitor.trees_area.tree_probes.main    import ProbesTree
from    opus.monitor.trees_area.tree_services.main  import ServicesTree

class TreeContainer(NFrameContainer):
    
    " the left tree area. Emit user clics events"

    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self._probesTree    = ProbesTree(self)
        self._servicesTree  = ServicesTree(self)
        self._grid = NGridContainer(self)
        #self._grid.setContentsMargins(6,0,2,0)
        self._grid.setVerticalSpacing(6)
        #self._grid.addWidget(self._commands,           0, 0)
        self._grid.addWidget(self._probesTree,         1, 0)
        self._grid.addWidget(self._servicesTree,       2, 0)

        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,2)
        self._grid.setRowStretch(2,1)
        self.setLayout(self._grid)
