# PySide
from    PySide.QtGui    import (
    QStackedLayout,
    QGridLayout
)
from noctopus_ramp import NSelector
from noctopus_widgets import NFrameContainer, NGrid, NFrame

class NCentralFrame(NFrame):

    " central widget container "

    def __init__(self, parent):
        super(NCentralFrame, self).__init__(parent)
        grid = NGrid(self)
        self.centralStack   = NCentralStack(self)
        self.selector       = NSelector(self, self.centralStack)
        grid.addWidget(self.selector,       0,0,0,1)
        grid.addWidget(self.centralStack,   0,1,1,1)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        self.selector.connectAll()
        self.setLayout(grid)

class NCentralStack(NFrameContainer):

    " main stack container "

    def __init__(self, parent):
        super(NCentralStack, self).__init__(parent)
        self._stack = QStackedLayout(self)
        self._stack.setContentsMargins(0,0,0,0)
        self._stackElements = dict()
        self.setLayout(self._stack)

    def selectEvent(self, app):
        self._stack.setCurrentWidget(self._stackElements[app])

    def addLayer(self, pyCallable, app):
        qWidget = pyCallable(self)
        self._stackElements[app] = qWidget
        self._stack.addWidget(qWidget)
