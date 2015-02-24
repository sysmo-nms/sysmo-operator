# PyQt5
from    PyQt5.QtCore   import QRect
from    PyQt5.QtGui    import (
    QPainter,
    QColor,
    QRadialGradient,
    QBrush
)
from    PyQt5.QtWidgets    import (
    QStackedLayout,
    QGridLayout,
    QLabel,
    QFrame
)
import sysmo_ramp
import sysmo_main
from sysmo_widgets import NFrameContainer, NGrid, NFrame

class NCentralFrame(NFrame):

    " central widget container "

    def __init__(self, parent):
        super(NCentralFrame, self).__init__(parent)
        NCentralFrame.singleton = self
        self.grid = NGrid(self)
        self.grid.setHorizontalSpacing(6)
        self.grid.setVerticalSpacing(6)
        self.centralStack   = NCentralStack(self)
        self.selector       = sysmo_ramp.NSelector(self, self.centralStack)
        #self.menuFrame  = NMenuFrame(self)
        #self.grid.addWidget(self.menuFrame,      0,0,1,2)
        self.grid.addWidget(self.selector,       1,0)
        self.grid.addWidget(self.centralStack,   1,1)

        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 1)
        self.selector.connectAll()
        self.setLayout(self.grid)

    def showInfo(self, boolean):
        if boolean == True:
            print("show info")
            self._infoFrame = NInfoFrame(self)
            self.grid.addWidget(self._infoFrame, 0,0,1,2)
        else:
            print("hide info")
            self.grid.removeWidget(self._infoFrame)
            self._infoFrame.deleteLater()

class NMenuFrame(NFrame):
    def __init__(self, parent):
        super(NMenuFrame, self).__init__(parent)
        grid = NGrid(self)
        self.setFrameShape(QFrame.StyledPanel)

        grid.addWidget(QLabel('overview', self), 0,0)
        grid.addWidget(QLabel('and menu', self), 1,0)
        self.setDisabled(True)
        self.setContentsMargins(3,4,4,4)

class NInfoFrame(NFrame):
    def __init__(self, parent):
        super(NInfoFrame, self).__init__(parent)
        self._parent = parent
        self._mousePos = None
        self._drawGradient = QRadialGradient()
        self._drawGradient.setRadius(500)
        self._drawGradient.setColorAt(0, QColor(100,100,100,0))
        self._drawGradient.setColorAt(1, QColor(100,100,100,111))
        self.setContentsMargins(0,0,0,0)
        self.setAcceptDrops(True)

    def paintEvent(self, event):
        rect    = event.rect()
        if self._mousePos != None:
            self._drawGradient.setCenter(self._mousePos)
            self._drawGradient.setFocalPoint(self._mousePos)
            brush = QBrush(self._drawGradient)
            QPainter(self).fillRect(rect, QBrush(self._drawGradient))
        else:
            QPainter(self).fillRect(rect, QColor(100,100,100,111))
        NFrame.paintEvent(self, event)

    def dragEnterEvent(self, event):
        event.accept()
        self._mousePos = event.pos()
        print("drag event! ")
        NFrame.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        print(("move", type(event)))
        self._mousePos = event.pos()
        self.update()
        NFrame.dragMoveEvent(self, event)

    def dropEvent(self, event):
        print(("drop event!", type(event)))
        self._parent.grid.removeWidget(self)
        self.deleteLater()
        NFrame.dropEvent(self, event)




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






