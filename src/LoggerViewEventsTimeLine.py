from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
import  TkorderIcons
import  Monitor

class EventsView(QFrame):
    def __init__(self, parent):
        super(EventsView, self).__init__(parent)
        #toolTipBaseHexa = Monitor.MonitorMain.singleton.rgbDict['Base']
        # self.setStyleSheet(
            #"QFrame { border-radius: 15px; background: %s}" % toolTipBaseHexa)
        height = 108
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
        height = height - 6

        self._vertiSpace    = height  / 6
        self._vertiStart    = -height / 2

        self._needRedraw = False
        self.setInteractive(False)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.extLine        = QGraphicsLineItem(QLine(0,0,0,0))
        #self.unknownLine    = QGraphicsLineItem(QLine(0,0,0,0))
        self.criticalLine   = QGraphicsLineItem(QLine(0,0,0,0))
        self.warningLine    = QGraphicsLineItem(QLine(0,0,0,0))
        self.okLine         = QGraphicsLineItem(QLine(0,0,0,0))

        backPen = QPen(QColor(Qt.lightGray))

        self.extLine.setPen(backPen)
        #self.unknownLine.setPen(backPen)
        self.criticalLine.setPen(backPen)
        self.warningLine.setPen(backPen)
        self.okLine.setPen(backPen)

        self.scene.addItem(self.extLine)
        #self.scene.addItem(self.unknownLine)
        self.scene.addItem(self.criticalLine)
        self.scene.addItem(self.warningLine)
        self.scene.addItem(self.okLine)

        self.extImage = QGraphicsSvgItem(TkorderIcons.getImage('dialog-information'))
        self.extImage.scale(0.37,0.37)

        self.okImage = QGraphicsSvgItem(TkorderIcons.getImage('weather-clear'))
        self.okImage.scale(0.37,0.37)

        self.warningImage = QGraphicsSvgItem(TkorderIcons.getImage('weather-showers'))
        self.warningImage.scale(0.37,0.37)

        self.criticalImage = QGraphicsSvgItem(TkorderIcons.getImage('weather-severe-alert'))
        self.criticalImage.scale(0.37,0.37)

        #self.unknownImage = QGraphicsSvgItem(TkorderIcons.getImage('weather-clear-night'))
        #self.unknownImage.scale(0.37,0.37)

        self.scene.addItem(self.extImage)
        self.scene.addItem(self.okImage)
        self.scene.addItem(self.warningImage)
        self.scene.addItem(self.criticalImage)
        #self.scene.addItem(self.unknownImage)


    def _scale(self):
        size    = self.size()
        width   = size.width() / 2 - 30
        leftWidth   = width 
        rightWidth  = width
        vertiSpace  = self._vertiSpace
        vertiStart  = self._vertiStart
        vertIconPadding = 9
        horiIconPadding = 24


        # draw background grid
        vert = vertiStart + vertiSpace
        self.extLine.setLine(       QLine(-leftWidth, vert, rightWidth, vert))
        self.extImage.setPos(QPointF(QPoint(-leftWidth -horiIconPadding, vert - vertIconPadding)))

        vert += vertiSpace
        #self.unknownLine.setLine(   QLine(-leftWidth, vert, rightWidth, vert))
        #self.unknownImage.setPos(QPointF(QPoint(-leftWidth -horiIconPadding, vert - vertIconPadding)))

        vert += vertiSpace
        self.criticalLine.setLine(  QLine(-leftWidth, vert, rightWidth, vert))
        self.criticalImage.setPos(QPointF(QPoint(-leftWidth -horiIconPadding, vert - vertIconPadding)))

        vert += vertiSpace
        self.warningLine.setLine(   QLine(-leftWidth, vert, rightWidth, vert))
        self.warningImage.setPos(QPointF(QPoint(-leftWidth -horiIconPadding, vert - vertIconPadding)))

        vert += vertiSpace
        self.okLine.setLine(        QLine(-leftWidth, vert, rightWidth, vert))
        self.okImage.setPos(QPointF(QPoint(-leftWidth -horiIconPadding, vert - vertIconPadding)))

        self.updateSceneRect(QRectF(0,0,width,112))
        self.centerOn(0,0)

        # TODO draw datas as large lines including tips on mouseover


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
