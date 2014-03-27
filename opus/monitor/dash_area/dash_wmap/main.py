from    PySide.QtGui        import QLabel
from    noctopus_widgets    import NFrameContainer, NGridContainer
from    opus.monitor.widgets    import OSMView

class WmapDash(NFrameContainer):
    def __init__(self, parent):
        super(WmapDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(OSMView(self), 0,0)
        self.setLayout(self._grid)
