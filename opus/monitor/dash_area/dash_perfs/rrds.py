from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    opus.monitor.proxy import (
    AbstractChannelWidget,
    ChanHandler
)
#from    CommonWidgets       import *
#from    LoggerViewRrds      import RrdArea
import  datetime
#import  TkorderIcons
from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtSvg    import *
import  platform
#import  MonitorDashboardArea
import  time
import  os
import  datetime
#import  TkorderIcons
import  nocapi
import  opus.monitor.api as monapi
#import  Monitor
#import  norrdQtThreaded
import  re
import  tempfile


class RrdArea(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdArea, self).__init__(parent, probe)
        self.probeName      = probe
        self.chanHandler    = ChanHandler.singleton
        self.probeConfig    = self.chanHandler.probes[probe]
        target = self.probeConfig['target']
        self.targetConfig   = self.chanHandler.targets[target]

        # text view on all types of probes

        # cartouche
        #self.cartoucheArea = QLabel(probe, self)
        grid = QGridLayout(self)

        self.textArea   = None
        self.rrdArea    = None
        # if there is a rrd logger
        if 'btracker_logger_rrd' in self.probeConfig['loggers'].keys():
            self.rrdArea = RrdFrame(self, self.probeConfig)
            grid.addWidget(self.rrdArea,  0,0,2,1)
            #grid.addWidget(self.cartoucheArea,  0,0,2,1)
            #grid.addWidget(self.textArea,       1,1,1,1)
            #grid.addWidget(self.rrdArea,        0,1,1,1)
            #grid.setRowStretch(1,0)
            #grid.setRowStretch(0,1)
        else:
            self.textArea   = QTextEdit(self)
            dtext           = QTextDocument()
            dtext.setMaximumBlockCount(500)
            tformat         = QTextCharFormat()
            tformat.setFontPointSize(8.2)
            self.textArea.setDocument(dtext)
            self.textArea.setCurrentCharFormat(tformat)
            self.textArea.setReadOnly(True)
            self.textArea.setLineWrapMode(QTextEdit.NoWrap)
            self.textArea.setFixedWidth(300)
            self.textArea.setFixedHeight(90)
            grid.addWidget(self.textArea,       0,0)

        self.setLayout(grid)
        self.connectProbe()

    def handleTextDump(self, data):
        self.textArea.append(str(data).rstrip())

    def handleReturn(self, value):
        tstamp  = value['timestamp'] / 1000000
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        printable = string.replace('\n', ' ').replace('  ', ' ')
        self.textArea.append(time + "-> " + printable)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'btracker_logger_text':
                if self.textArea != None:
                    for line in msg['data']:
                        self.textArea.append(str(line).rstrip())
            elif msg['logger'] == 'btracker_logger_rrd':
                if self.rrdArea != None: 
                    self.rrdArea.rrdDump(msg['data'])
        elif msg['msgType'] == 'probeReturn':
            if self.textArea != None:
                self.handleReturn(msg['value'])
            if self.rrdArea != None:
                self.rrdArea.updateGraph()

class RrdFrame(QFrame):
    def __init__(self, parent, probeDict, headThumb=None):
        super(RrdFrame, self).__init__(parent)
        self.headThumb = headThumb
        self.setMinimumWidth(600)
        self.knownHeight    = 0
        self.knownWidth     = 0
        self.probeDict      = probeDict
        self.rrdConf        = self.probeDict['loggers']['btracker_logger_rrd']
        self.rrdViews = dict()

        #self.timelineSlider = MonitorDashboardArea.Dashboard.singleton.timelineSlide
        #self.stopSlider     = MonitorDashboardArea.Dashboard.singleton.stopSlide
        #timeline = self.timelineSlider.value()
        #stop     = self.stopSlider.value()
        timeline  = 3600
        stop      = 0

        #MonitorDashboardArea.Dashboard.singleton.timelineSlide.sliderReleased.connect(self.timelineChanged)
        #MonitorDashboardArea.Dashboard.singleton.stopSlide.sliderReleased.connect(self.stopChanged)

        grid        = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        rowCount    = 0
        self.setFixedHeight(len(self.rrdConf) * 200)

        for key in self.rrdConf:
            self.rrdViews[key] = RrdView(self, key, self.rrdConf[key], timeline, stop)
            grid.addWidget(self.rrdViews[key], rowCount, 0)
            rowCount += 1

    def thumbUpdate(self, filename):
        if self.headThumb != None:
            self.headThumb.setThumbnail(filename)

    def timelineChanged(self):
        for key in self.rrdViews:
            self.rrdViews[key].updateTimeline(self.timelineSlider.value())

    def stopChanged(self):
        for key in self.rrdViews:
            self.rrdViews[key].updateStop(self.stopSlider.value())

    def rrdDump(self, fileDict):
        self._rrdfileReady  = True
        self.rrdFileDict    = fileDict
        for key in fileDict:
            self.rrdViews[key].setRrdFile(fileDict[key])
        self.updateGraph()

    def updateGraph(self):
        for key in self.rrdViews:
            self.rrdViews[key].updateGraph()

class RrdView(QLabel):
    def __init__(self, parent, key, confDict, timeline, stop):
        super(RrdView, self).__init__(parent)
        self.parent = parent
        self.fileId = key
        self.config = confDict
        self.timeline = timeline
        self.stop = stop
        self.rrdGraphConf = confDict['graphs'][0]
        #self.hexaPalette     = Monitor.MonitorMain.singleton.rgbaDict
        self._needRedraw     = False
        self._rrdfileReady   = False
        rrdFile = QTemporaryFile(self)
        rrdFile.open()
        rrdFile.close()
        rrdThumb = QTemporaryFile(self)
        rrdThumb.open()
        rrdThumb.close()
        self.rrdGraphFileName = rrdFile.fileName()
        self.rrdThumbFileName = rrdThumb.fileName()

    def setRrdFile(self, fileName):
        self._rrdfileReady  = True
        if platform.system() == 'Windows':
            # DS can be read by rrdtool windows only on files formated like:
            # C\:\\bla\\bla\\bla.rrd. XXX WTF XXX
            self.rrdFile = fileName.replace("/", "\\\\").replace(":", "\\:")
        else:
            self.rrdFile = fileName

        self.rrdGraphConf = re.sub('<FILE>',self.rrdFile, self.rrdGraphConf)

    def updateTimeline(self, value):
        self.timeline = value
        self.updateGraph()

    def updateStop(self, value):
        self.stop = value
        self.updateGraph()

    def resizeEvent(self, event):
        if self._rrdfileReady == True:
            self._needRedraw = True
        QLabel.resizeEvent(self, event)

    def paintEvent(self, event):
        if self._needRedraw == True:
            self.updateGraph()
            self._needRedraw = False
        QLabel.paintEvent(self, event)

    def updateGraph(self):

        defs    = re.findall(r'DEF:[^\s]+', self.rrdGraphConf)
        lines   = re.findall(r'LINE[^\s]+', self.rrdGraphConf)
        areas   = re.findall(r'AREA[^\s]+', self.rrdGraphConf)

        size = self.size()
        rrdWidth  = size.width()
        rrdHeight = size.height()
        rrdStart  = self.timeline
        rrdStop   = time.time() / 1 + self.stop

        if self.isVisible() == False:
            cmd = self._generateThumbCmd(rrdStart, rrdStop, defs, lines, areas, rrdWidth, rrdHeight)
            monapi.rrdDraw(cmd, self._thumbComplete)
            #ret = norrdQtThreaded.cmd(cmd, self._thumbComplete)
        else:
            cmd = self._generateGraphCmd(rrdStart, rrdStop, defs, lines, areas, rrdWidth, rrdHeight)
            monapi.rrdDraw(cmd, self._graphComplete)
            #ret = norrdQtThreaded.cmd(cmd, self._graphComplete)

    def _thumbComplete(self, msg):
        self.parent.thumbUpdate(self.rrdThumbFileName)

    def _graphComplete(self, msg):
        self.setPixmap(QPixmap(self.rrdGraphFileName))

    
    def _generateGraphCmd(self, rrdStart, rrdStop, defs, lines, areas, w, h):
        head = 'graph %s --imgformat PNG --width %s --height %i ' % (self.rrdGraphFileName, w, h)
        opts = '--full-size-mode --disable-rrdtool-tag --slope-mode --tabwidth 40 --watermark %s' % 'watermark '
        #opts = '--full-size-mode --disable-rrdtool-tag --border 0 --dynamic-labels --slope-mode --tabwidth 40 --watermark %s' % 'watermark '
        colors = '--color BACK#00000000 --color CANVAS%s --color GRID%s --color MGRID%s --color FONT%s --color AXIS%s --color FRAME%s --color ARROW%s ' % (
                nocapi.nGetRgba('Base'),
                nocapi.nGetRgba('Dark'),
                nocapi.nGetRgba('Shadow'),
                nocapi.nGetRgba('WindowText'),
                nocapi.nGetRgba('Dark'),
                nocapi.nGetRgba('Window'),
                nocapi.nGetRgba('Shadow')
            )
        time = '--start end-%i --end %i ' % (rrdStart, rrdStop)
        defsC = ''
        for i in range(len(defs)):
            defsC += ' %s ' % defs[i]

        linesC = ''
        for i in range(len(lines)):
            linesC += ' %s ' % lines[i]

        areasC = ''
        for i in range(len(areas)):
            areasC += ' %s ' % areas[i]

        cmd = head + opts + colors + time + defsC + linesC + areasC
        return cmd

    def _generateThumbCmd(self, rrdStart, rrdStop, defs, lines, areas, w, h):
        head = 'graph %s --imgformat PNG --width 90 --height 30 ' % self.rrdThumbFileName
        opts = '--only-graph --rigid --slope-mode --tabwidth 40 --watermark %s' % 'watermark '
        colors = '--color BACK#00000000 --color CANVAS%s --color GRID%s --color MGRID%s --color FONT%s --color AXIS%s --color FRAME%s --color ARROW%s ' % (
                self.hexaPalette['Base'],
                self.hexaPalette['Dark'],
                self.hexaPalette['Shadow'],
                self.hexaPalette['WindowText'],
                self.hexaPalette['Dark'],
                self.hexaPalette['Window'],
                self.hexaPalette['Shadow']
            )
        time = '--start end-%i --end %i ' % (rrdStart, rrdStop)
        defsC = ''
        for i in range(len(defs)):
            defsC += ' %s ' % defs[i]

        linesC = ''
        for i in range(len(lines)):
            linesC += ' %s ' % lines[i]

        areasC = ''
        for i in range(len(areas)):
            areasC += ' %s ' % areas[i]

        cmd = head + opts + colors + time + defsC + linesC + areasC
        return cmd
