from    PySide.QtGui        import (
    QTabWidget,
    QMdiArea,
    QFrame
)
from    noctopus_widgets    import (
    NFrame,
    NGrid
)
from    opus.monitor.dash_area.controls import DashActions
from    opus.monitor.dash_area.dash     import Dashboard

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

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        self.addTab(Dashboard(self), 'Default')
        #self.setFrameShape(QFrame.StyledPanel)
        #self.setContentsMargins(6,4,2,4)
        #self._grid      = NGrid(self)
        #self._controls  = DashActions(self)
        #self._grid.addWidget(self._controls,    0,0)
