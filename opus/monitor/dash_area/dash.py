from    PySide.QtGui        import (
    QTabWidget,
    QMdiArea
)
from    noctopus_widgets    import (
    NFrame,
    NGrid
)

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        self.addTab(DashView(self), 'Default')
        #self.setFrameShape(QFrame.StyledPanel)
        #self.setContentsMargins(6,4,2,4)
        #self._grid      = NGrid(self)
        #self._controls  = DashActions(self)
        #self._grid.addWidget(self._controls,    0,0)

class DashView(QMdiArea):
    def __init__(self, parent):
        super(DashView, self).__init__(parent)
