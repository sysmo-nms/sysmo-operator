from    PySide.QtGui        import QLabel
from    noctopus_widgets    import NFrameContainer, NGridContainer

class WmapDash(NFrameContainer):
    def __init__(self, parent):
        super(WmapDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QLabel('wmap', self), 0,0)
        self.setLayout(self._grid)
