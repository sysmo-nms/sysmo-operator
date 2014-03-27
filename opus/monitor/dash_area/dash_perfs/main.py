from    PySide.QtGui        import QTreeWidget
from    noctopus_widgets    import NFrameContainer, NGridContainer

class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QTreeWidget(self), 0,0)
        self.setLayout(self._grid)
