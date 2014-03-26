from    PySide.QtGui        import QFrame
from    noctopus_widgets    import (
    NFrame,
    NGrid
)
from    opus.monitor.dash_area.controls import DashActions
from    opus.monitor.dash_area.dash     import DashTab

class DashContainer(NFrame):
    def __init__(self, parent):
        super(DashContainer, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setContentsMargins(6,4,2,4)
        self._controls  = DashActions(self)
        self._tabs      = DashTab(self)

        self._grid      = NGrid(self)
        self._grid.setVerticalSpacing(6)
        self._grid.addWidget(self._controls,    0,0)
        self._grid.addWidget(self._tabs,        1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)
