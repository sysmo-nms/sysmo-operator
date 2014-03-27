from    PySide.QtGui        import QTreeWidget
from    noctopus_widgets    import NFrameContainer, NGridContainer

class BrowserDash(NFrameContainer):
    def __init__(self, parent):
        super(BrowserDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(QTreeWidget(self), 0,0)
        self.setLayout(self._grid)
