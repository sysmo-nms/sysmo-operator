from    PyQt5.QtWidgets        import QLabel
from    sysmo_widgets    import NFrameContainer, NGridContainer
from    dashboard.dash_widgets    import OSMView

class WmapDash(NFrameContainer):
    def __init__(self, parent):
        super(WmapDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(OSMView(self), 0,0)
        self.setLayout(self._grid)
