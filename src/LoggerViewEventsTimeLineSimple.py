from    PySide.QtGui        import *
from    PySide.QtCore       import *
import  MonitorDashboardArea
import  operator
import  time

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

        self.eventDatas             = list()
        self._initSliders()

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'tracker_events':
                self._synchronizeData(msg)
                self._updateGraph()
        elif msg['msgType'] == 'probeReturn':
            self._updateData(msg)
            self._updateGraph()

    def _synchronizeData(self, msg):
        data            = msg['data']
        data.sort(key=operator.itemgetter('insertTs'))
        self.eventDatas = data
        for l in self.eventDatas:
            print l['insertTs'] / 1000000, l['status']

    def _updateData(self, msg): pass

    def _updateGraph(self):
        figureWidth     = self.size().width()

        secondRange     = self.timeRange
        secondFromNow   = self.stopTime
        timeNow         = int(time.time())
        tsEnd           = timeNow + secondFromNow
        tsStart         = tsEnd - secondRange

        #print secondRange, " ", secondFromNow, " ", figureWidth, " ", timeNow
        print 'graph will start ad ', tsStart, ' and end at ', tsEnd

        print self
        for i in range(len(self.eventDatas)):
            ts = self.eventDatas[i]['insertTs'] / 1000000
            if ts > tsStart and ts < tsEnd:
                print ts

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
    
    # Time range and stop time controls
    def _initSliders(self):
        self.timeRangeSlider = MonitorDashboardArea.Dashboard.singleton.timelineSlide
        self.stopTimeSlider  = MonitorDashboardArea.Dashboard.singleton.stopSlide

        self.timeRangeSlider.sliderReleased.connect(self._timeRangeChanged)
        self.stopTimeSlider.sliderReleased.connect(self._stopTimeChanged)

        self.stopTime   = self.stopTimeSlider.value()
        self.timeRange  = self.timeRangeSlider.value()
        self._updateGraph()

    def _stopTimeChanged(self):
        self.stopTime   = self.stopTimeSlider.value()
        self._updateGraph()
        print 'stop time changed'

    def _timeRangeChanged(self):
        self.timeRange  = self.timeRangeSlider.value()
        self._updateGraph()
        print 'time range changed'
