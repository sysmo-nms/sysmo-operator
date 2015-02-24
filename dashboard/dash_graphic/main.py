from    PyQt5.QtWidgets        import QGraphicsScene, QGraphicsView
from    sysmo_widgets    import NFrameContainer, NGridContainer

class GraphicDash(NFrameContainer):
    def __init__(self, parent):
        super(GraphicDash, self).__init__(parent)
        self._view  = QGraphicsView(self)
        self._grid = NGridContainer(self)
        self._grid.addWidget(self._view, 0,0)
        self.setLayout(self._grid)
