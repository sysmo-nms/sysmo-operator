# PySide
from    PySide.QtCore   import QRect
from    PySide.QtGui    import (
    QStackedLayout,
    QGridLayout,
    QPainter,
    QColor
)
import noctopus_ramp
from noctopus_widgets import NFrameContainer, NGrid, NFrame

class NCentralFrame(NFrame):

    " central widget container "

    def __init__(self, parent):
        super(NCentralFrame, self).__init__(parent)
        NCentralFrame.singleton = self
        self._grid = NGrid(self)
        self._grid.setHorizontalSpacing(2)
        self.centralStack   = NCentralStack(self)
        self.selector       = noctopus_ramp.NSelector(self, self.centralStack)
        self._grid.addWidget(self.selector,       0,0,)
        self._grid.addWidget(self.centralStack,   0,1,)
        self._grid.setColumnStretch(0, 0)
        self._grid.setColumnStretch(1, 1)
        self.selector.connectAll()
        self.setLayout(self._grid)

    def showInfo(self, boolean):
        if boolean == True:
            print "show info"
            self._infoFrame = NInfoFrame(self)
            self._grid.addWidget(self._infoFrame, 0,0,1,2)
        else:
            print "hide info"
            self._grid.removeWidget(self._infoFrame)
            self._infoFrame.deleteLater()


class NInfoFrame(NFrame):
    def __init__(self, parent):
        super(NInfoFrame, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
        self.setAcceptDrops(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect    = event.rect()
        painter.fillRect(rect, QColor(100,100,100,50))
        NFrame.paintEvent(self, event)

    def dragEnterEvent(self, event):
        event.accept()
        print "drag event! "

    def dropEvent(self, event):
        print "drop event!", type(event)
        self.deleteLater()




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
