from    PySide.QtGui        import QLabel
from    noctopus_widgets    import NFrameContainer, NGridContainer

class TimelineDash(NFrameContainer):
    def __init__(self, parent):
        super(TimelineDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QLabel('timeline', self), 0,0)
        self.setLayout(self._grid)
