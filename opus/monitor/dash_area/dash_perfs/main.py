from    PySide.QtGui        import QLabel
from    noctopus_widgets    import NFrameContainer, NGridContainer

class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QLabel('perf', self), 0,0)
        self.setLayout(self._grid)
