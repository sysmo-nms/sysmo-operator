from    PyQt5.QtGui        import QListWidget
from    noctopus_widgets    import NFrameContainer, NGridContainer

class TimelineDash(NFrameContainer):
    def __init__(self, parent):
        super(TimelineDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QListWidget(self), 0,0)
        self.setLayout(self._grid)
