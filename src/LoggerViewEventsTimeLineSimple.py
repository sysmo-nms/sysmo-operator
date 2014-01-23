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
        #for l in self.eventDatas:
        #    print l['insertTs'] / 1000000, l['status']

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

    def _drawContainer(self):
        border  = QRect(0.0,0.0,self.widgetWidth,self.widgetHeight)
        painter = QPainter(self)
        painter.setPen(self.darkColor)
        painter.setBrush(self.borderBrush)
        painter.drawRoundRect(border, 5,5)

    def _drawTimeLines(self):
        figureTics      = self.tsEnd - self.tsStart
        figurePix       = self.size().width()
        ticsPerPix      = figureTics / figurePix
        print "total  tics: ", figureTics
        print "figure pix:  ", figurePix
        print "tics per pixel: ", ticsPerPix

        toDrawFromEnd   = list()
        selLen          = len(self.selection)
        remainingPix    = figurePix

        print len(self.selection)

        for i in range(len(self.selection)):
            eventTs     = self.selection[i]['insertTs']     / 1000000
            if i == 0: 
                # last event
                totalTics   = self.timeNow - eventTs
                totalPix    = totalTics / ticsPerPix
                #print remainingPix, totalPix, totalTics
                remainingPix = remainingPix - totalPix
            elif i == selLen - 1:
                # first out of bound event, with will be the remaining
                # available pixels
                #print remainingPix
                totalPix    = remainingPix
            else:
                nextEventTs = self.selection[i - 1]['insertTs'] / 1000000
                totalTics   = nextEventTs - eventTs
                totalPix    = totalTics / ticsPerPix
                #print remainingPix
                remainingPix = remainingPix - totalPix
            
            anEvent = dict()
            anEvent['pixWidth']     = totalPix
            anEvent['status']       = self.selection[i]['status']
            toDrawFromEnd.append(anEvent)

        #print toDrawFromEnd


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
