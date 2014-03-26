from    PySide.QtGui        import QLabel
from    noctopus_widgets    import NFrameContainer, NGridContainer

class GraphicDash(NFrameContainer):
    def __init__(self, parent):
        super(GraphicDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QLabel('graphic', self), 0,0)
        self.setLayout(self._grid)
