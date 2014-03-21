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

        self.alpha0      = pal.color(QPalette.Normal, QPalette.Dark)
        self.alpha1      = pal.color(QPalette.Normal, QPalette.Dark)
        self.alpha0.setAlpha(150)
        self.alpha1.setAlpha(1)

        self.widgetHeight       = 15 
        self.timeLineHeight     = self.widgetHeight - 2
        self.widgetHeightHint   = self.widgetHeight + 1

        self.widgetWidth        = 80
        self.widgetWidthHint    = self.widgetWidth + 1

        self.borderBrush            = QBrush(self.windowColor)
        self.timeLineUnknownBrush   = QBrush(self.darkColor)
        
        self.tsEnd      = None
        self.tsStart    = None
        self.timeNow    = None
        self.selection  = None

        self.eventDatas = list()
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

    def _updateData(self, msg): pass

    def _updateGraph(self):

        secondRange     = self.timeRange
        secondFromNow   = self.stopTime
        timeNow         = int(time.time())
        tsEnd           = timeNow + secondFromNow
        tsStart         = tsEnd - secondRange

        self.tsEnd      = tsEnd
        self.tsStart    = tsStart
        self.timeNow    = timeNow
        self.selection = list()
        for val in reversed(self.eventDatas):
            ts = val['insertTs'] / 1000000
            if ts < tsEnd and ts > tsStart:
                self.selection.append(val)
            else:
                # add the last past out of bound event and
                # no need to go further.
                self.selection.append(val)
                break
 
        self.update()

    # QWidget custom painting
    def sizeHint(self):
        return QSize(self.widgetWidthHint, self.widgetHeightHint)

    def resizeEvent(self, resizeEvent):
        self.widgetWidth    = resizeEvent.size().width() - 1
        self.timeLineWidth  = resizeEvent.size().width() - 3

        QWidget.resizeEvent(self, resizeEvent)

    def paintEvent(self, paintEvent):
        self._drawContainer()
        if self.selection != None:
            self._drawTimeLines()
        self._drawGradient()

    def _drawContainer(self):
        border  = QRect(0.0,0.0,self.widgetWidth,self.widgetHeight)
        painter = QPainter(self)
        painter.setPen(self.darkColor)
        painter.setBrush(self.borderBrush)
        painter.drawRoundRect(border, 5,5)

    def _drawTimeLines(self):
        figureTics      = self.tsEnd - self.tsStart
        figurePix       = self.size().width()
        ticsPerPix      = float(figureTics) / float(figurePix)

        selLen          = len(self.selection)
        remainingPix    = figurePix

        toDrawFromEnd   = list()
        firstPass       = True
        for i in range(len(self.selection)):
            eventTs     = self.selection[i]['insertTs']     / 1000000
            if selLen == 1: 
                # last value, only one value, unique pass
                totalPix = remainingPix
            if i == 0:
                # last value, use timeNow to mesure the timeTics
                totalTics    = self.timeNow - self.selection[i]['insertTs'] / 1000000
                totalPix     = totalTics / ticsPerPix
                remainingPix = remainingPix - totalPix
            elif i == selLen - 1:
                # first value, all remaining pix go here
                totalPix = remainingPix
            else:
                nextEventTs = self.selection[i - 1]['insertTs'] / 1000000
                totalTics   = nextEventTs - eventTs
                totalPix    = totalTics / ticsPerPix
                remainingPix = remainingPix - totalPix
 
            anEvent = dict()
            anEvent['pixWidth']     = totalPix
            anEvent['status']       = self.selection[i]['status']
            toDrawFromEnd.append(anEvent)

        startLeft = 1
        painter = QPainter(self)
        for val in reversed(toDrawFromEnd):
            r = QRect(startLeft, 1, val['pixWidth'], self.timeLineHeight)
            startLeft = startLeft + val['pixWidth']
            if val['status'] == 'OK':
                color = QColor(161,217,155)
                painter.setPen(color)
                painter.setBrush(color)
            elif val['status'] == 'UNKNOWN':
                painter.setPen(self.windowColor)
                painter.setBrush(self.timeLineUnknownBrush)
            elif val['status'] == 'CRITICAL':
                color = QColor(239,29,29)
                painter.setPen(color)
                painter.setBrush(color)
            elif val['status'] == 'WARNING':
                color = QColor(252,175,62)
                painter.setPen(color)
                painter.setBrush(color)
            painter.drawRoundRect(r, 5,5)

    def _drawGradient(self):
        border  = QRect(0.0,0.0,self.widgetWidth,self.widgetHeight)
        startHeight = self.widgetHeight / 2
        painter = QPainter(self)
        gradiant = QLinearGradient(1,startHeight,self.widgetWidth,startHeight)
        gradiant.setColorAt(0, self.alpha0)
        gradiant.setColorAt(1, self.alpha1)
        brush = QBrush(gradiant)
        painter.setPen(self.darkColor)
        painter.setBrush(brush)
        painter.drawRoundRect(border, 5,5)

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
