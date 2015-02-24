from    PyQt5.QtCore   import (
    Qt,
    QRectF,
)
from    PyQt5.QtGui   import (
    QPalette
)
from    PyQt5.QtWidgets   import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsItem,
    QGraphicsDropShadowEffect,
    QLabel,
    QWidget,
    QGridLayout,
)

import  sysmapi

class MDIDependencies(QGraphicsView):
    def __init__(self, parent):
        super(MDIDependencies, self).__init__(parent)
        self.setScene(DependenciesScene(self))

    def _addRootElement(self):
        self._scene.addWidget(QLabel('root'),wFlags=Qt.Dialog)

class DependenciesScene(QGraphicsScene):
    def __init__(self, parent):
        super(DependenciesScene, self).__init__(parent)
        # TOPYQT( ERROR BEGIN
        #self.setBackgroundBrush(self.palette().color(QPalette.Dark))
        #widget  = TargetItem('target1')
        #widget2 = TargetItem('target2')
        #self.addWidget(widget, Qt.Dialog | Qt.WindowTitleHint)
        #self.addWidget(widget2, Qt.Dialog | Qt.WindowTitleHint)
        #i1 = SimpleItem()
        #i2 = SimpleItem()
        #self.addItem(i1)
        #self.addItem(i2)
        #self.addLine(0,0,100,100)
        # TOPYQT( ERROR END


class SimpleItem(QGraphicsItem):
    def __init__(self, parent=None, scene=None):
        super(SimpleItem, self).__init__(parent,scene)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(
                -10 - penWidth / 2,
                -10 - penWidth / 2,
                 20 + penWidth,
                 20 + penWidth)

    def paint(self, painter, option, widget):
        painter.drawRoundedRect(-10, -10, 20, 20, 5, 5)


class TargetItem(QWidget):
    def __init__(self, name, parent=None):
        super(TargetItem, self).__init__(parent)
        grid = QGridLayout(self)
        grid.addWidget(QLabel(name,self), 0,0)
