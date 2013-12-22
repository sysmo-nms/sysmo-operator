from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtSvg    import *
import  MonitorDashboardArea
import  time
import  os
import  datetime
import  TkorderIcons
import  Monitor
import  rrdtool
import  re
import  tempfile

class RrdArea(QFrame):
    def __init__(self, parent, probeDict):
        super(RrdArea, self).__init__(parent)
        self.setMinimumWidth(600)
        self.knownHeight    = 0
        self.knownWidth     = 0
        self.probeDict      = probeDict
        self.rrdConf        = self.probeDict['loggers']['btracker_logger_rrd']
        self.rrdViews = dict()

        self.timelineSlider = MonitorDashboardArea.Dashboard.singleton.timelineSlide
        self.stopSlider     = MonitorDashboardArea.Dashboard.singleton.stopSlide
        timeline = self.timelineSlider.value()
        stop     = self.stopSlider.value()

        MonitorDashboardArea.Dashboard.singleton.timelineSlide.sliderReleased.connect(self.timelineChanged)
        MonitorDashboardArea.Dashboard.singleton.stopSlide.sliderReleased.connect(self.stopChanged)

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
        self.fileId = key
        self.config = confDict
        self.timeline = timeline
        self.stop = stop
        self.rrdGraphConf = confDict['graphs'][0]
        self.hexaPalette    = Monitor.MonitorMain.singleton.rgbaDict
        self._needRedraw     = False
        self._rrdfileReady   = False
        rrdFile = QTemporaryFile(self)
        rrdFile.open()
        rrdFile.close()
        self.rrdGraphFileName = rrdFile.fileName()

    def setRrdFile(self, fileName):
        self._rrdfileReady  = True
        self.rrdFile        = fileName
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
        if self.isVisible() == False: return

        defs    = re.findall(r'DEF:[^\s]+', self.rrdGraphConf)
        lines   = re.findall(r'LINE[^\s]+', self.rrdGraphConf)
        areas   = re.findall(r'AREA[^\s]+', self.rrdGraphConf)

        size = self.size()
        rrdWidth  = size.width()
        rrdHeight = size.height()
        rrdStart  = self.timeline
        rrdStop   = time.time() / 1 + self.stop

        # python rrdtool did not support list of DEFs or LINEs in the module
        # args. This lead to generate the function as string and evaluate
        # it with eval().
        cmd = "rrdtool.graph(str(self.rrdGraphFileName), \
            '--imgformat', 'PNG', \
            '--width', str(rrdWidth), \
            '--height', str(rrdHeight), \
            '--full-size-mode', \
            '--border', '0', \
            '--dynamic-labels', \
            '--slope-mode', \
            '--tabwidth', '40', \
            '--watermark', 'Watermark', \
            '--color', 'BACK#00000000',  \
            '--color', 'CANVAS%s'   % self.hexaPalette['Base'], \
            '--color', 'GRID%s'     % self.hexaPalette['Dark'], \
            '--color', 'MGRID%s'    % self.hexaPalette['Shadow'], \
            '--color', 'FONT%s'     % self.hexaPalette['WindowText'], \
            '--color', 'AXIS%s'     % self.hexaPalette['Dark'], \
            '--color', 'FRAME%s'    % self.hexaPalette['Window'], \
            '--color', 'ARROW%s'    % self.hexaPalette['Shadow'], \
            '--start', 'end-%i'     % rrdStart, \
            '--end',   '%i'         % rrdStop,"

        for i in range(len(defs)):
            cmd += "'%s'," % defs[i]
        for i in range(len(lines)):
            cmd += "'%s'," % lines[i]
        for i in range(len(areas)):
            cmd += "'%s'," % areas[i]

        cmd = re.sub(r',$', ')\n', cmd)
        eval(cmd)
        picture = QPixmap(self.rrdGraphFileName)
        self.setPixmap(picture)
