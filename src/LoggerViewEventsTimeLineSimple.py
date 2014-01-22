from    PySide.QtGui        import *
from    PySide.QtCore       import *
import operator

class SimpleTimeLine(QWidget):
    def __init__(self, parent):
        super(SimpleTimeLine, self).__init__(parent)
        pal = QPalette()
        self.windowColor = pal.color(QPalette.Normal, QPalette.Window)
        self.altColor    = pal.color(QPalette.Normal, QPalette.AlternateBase)
        self.baseColor   = pal.color(QPalette.Normal, QPalette.Base)
        self.darkColor   = pal.color(QPalette.Normal, QPalette.Dark)

        self.widgetHeight       = 20
        self.timeLineHeight     = self.widgetHeight - 2
        self.widgetHeightHint   = self.widgetHeight + 1

        self.widgetWidth        = 80
        self.widgetWidthHint    = self.widgetWidth + 1

        self.borderBrush            = QBrush(self.windowColor)
        self.timeLineUnknownBrush   = QBrush(self.darkColor)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'tracker_events':
                self._synchronizeTimeLine(msg)
        elif msg['msgType'] == 'probeReturn':
            self._updateTimeLine(msg)

    def _synchronizeTimeLine(self, msg):
        data            = msg['data']
        data.sort(key=operator.itemgetter('insertTs'))
        self.eventDatas = data
        for l in self.eventDatas:
            print l['insertTs'] / 1000000, l['status']

    def _updateTimeLine(self, msg): pass

    # QWidget custom painting
    def sizeHint(self):
        return QSize(self.widgetWidthHint, self.widgetHeightHint)

    def resizeEvent(self, resizeEvent):
        self.widgetWidth    = resizeEvent.size().width() - 1
        self.timeLineWidth  = resizeEvent.size().width() - 3

        QWidget.resizeEvent(self, resizeEvent)

    def paintEvent(self, paintEvent):
        self._drawContainer()
        self._drawTimeLines()

    def _drawContainer(self):
        border  = QRect(0.0,0.0,self.widgetWidth,self.widgetHeight)
        painter = QPainter(self)
        painter.setPen(self.darkColor)
        painter.setBrush(self.borderBrush)
        painter.drawRoundRect(border, 5,5)

    def _drawTimeLines(self):
        atimeLine = QRect(1,1,80,self.timeLineHeight)
        painter = QPainter(self)
        painter.setPen(self.altColor)
        painter.setBrush(self.timeLineUnknownBrush)
        painter.drawRoundRect(atimeLine, 5,5)
