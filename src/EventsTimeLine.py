from    PySide.QtGui        import *
from    PySide.QtCore       import *
import  Monitor

class EventsView(QFrame):
    def __init__(self, parent):
        super(EventsView, self).__init__(parent)
        #toolTipBaseHexa = Monitor.MonitorMain.singleton.rgbDict['Base']
        # self.setStyleSheet(
            #"QFrame { border-radius: 15px; background: %s}" % toolTipBaseHexa)
        height = 112
        self.setFixedHeight(height)
        grid = QGridLayout(self)
        self.graphicsView = EventsViewGraphicScene(self, height)
        grid.addWidget(self.graphicsView, 0,0)
        self.setLayout(grid)

class EventsViewGraphicScene(QGraphicsView):
    def __init__(self, parent, height):
        super(EventsViewGraphicScene, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._vertiSpace    = height  / 7
        self._vertiStart    = -height / 2

        self._needRedraw = False
        self.setInteractive(False)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.extLine        = QGraphicsLineItem(QLine(0,0,0,0))
        self.okLine         = QGraphicsLineItem(QLine(0,0,0,0))
        self.warningLine    = QGraphicsLineItem(QLine(0,0,0,0))
        self.criticalLine   = QGraphicsLineItem(QLine(0,0,0,0))
        self.unknownLine    = QGraphicsLineItem(QLine(0,0,0,0))
        self.stealthLine    = QGraphicsLineItem(QLine(0,0,0,0))

        self.scene.addItem(self.okLine)
        self.scene.addItem(self.warningLine)
        self.scene.addItem(self.criticalLine)
        self.scene.addItem(self.unknownLine)
        self.scene.addItem(self.stealthLine)

    def _scale(self):
        size    = self.size()
        width   = size.width() / 2 - 30
        leftWidth   = width 
        rightWidth  = width
        vertiSpace  = self._vertiSpace
        vertiStart  = self._vertiStart

        vert = vertiStart + vertiSpace
        self.extLine.setLine(       QLine(-leftWidth, vert, rightWidth, vert))
        vert += vertiSpace
        self.okLine.setLine(        QLine(-leftWidth, vert, rightWidth, vert))
        vert += vertiSpace
        self.warningLine.setLine(   QLine(-leftWidth, vert, rightWidth, vert))
        vert += vertiSpace
        self.criticalLine.setLine(  QLine(-leftWidth, vert, rightWidth, vert))
        vert += vertiSpace
        self.unknownLine.setLine(   QLine(-leftWidth, vert, rightWidth, vert))
        vert += vertiSpace
        self.stealthLine.setLine(   QLine(-leftWidth, vert, rightWidth, vert))

        self.updateSceneRect(QRectF(0,0,width,112))
        self.centerOn(0,0)


    def resizeEvent(self, event):
        print "resizeEvent"
        self._needRedraw = True
        QGraphicsView.resizeEvent(self, event)

    def paintEvent(self, event):
        print "PainEvent"
        if self._needRedraw == True:
            print "need redraw"
            self._scale()
            self._needRedraw = False
        QGraphicsView.paintEvent(self, event)
