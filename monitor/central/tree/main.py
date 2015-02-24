from    PyQt5.QtWidgets     import QFrame
from    sysmo_widgets import (NFrame, NGrid)

from    monitor.central.tree.controls      import ElementsActions
from    monitor.central.tree.tree_view     import ProbesTreeview

class ProbesTree(NFrame):
    def __init__(self, parent):
        super(ProbesTree, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self._grid = NGrid(self)
        self._probesActions     = ElementsActions(self)
        self._probesTreeview    = ProbesTreeview(self)
        self._connectControls()
        self._grid.addWidget(self._probesActions,   0,0)
        self._grid.addWidget(self._probesTreeview,  1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

    def _connectControls(self):
        self._probesActions.line.textChanged.connect(
            self._probesTreeview.filterThis
        )
