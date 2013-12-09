from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtSvg    import *
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
        self.setStyleSheet("QFrame { background: #999999 }")
        self.setMinimumWidth(600)
        self.knownHeight    = 0
        self.knownWidth     = 0
        self.probeDict      = probeDict
        self.rrdConf        = self.probeDict['loggers']['btracker_logger_rrd']
        self.rrdViews = dict()

        grid        = QGridLayout(self)
        rowCount    = 0
        for key in self.rrdConf:
            self.rrdViews[key] = RrdView(self, key, self.rrdConf[key])
            grid.addWidget(self.rrdViews[key], rowCount, 0)
            rowCount += 1

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
    def __init__(self, parent, key, confDict):
        super(RrdView, self).__init__(parent)
        self.fileId = key
        self.config = confDict
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
        rrdStart  = 3600 

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
            '--color', 'BACK%s'     % self.hexaPalette['Window'], \
            '--color', 'CANVAS%s'   % self.hexaPalette['Base'], \
            '--color', 'GRID%s'     % self.hexaPalette['Dark'], \
            '--color', 'MGRID%s'    % self.hexaPalette['Shadow'], \
            '--color', 'FONT%s'     % self.hexaPalette['WindowText'], \
            '--color', 'AXIS%s'     % self.hexaPalette['Dark'], \
            '--color', 'FRAME%s'    % self.hexaPalette['Window'], \
            '--color', 'ARROW%s'    % self.hexaPalette['Shadow'], \
            '--start', '-%i' % rrdStart, \
            '--end', 'now',"

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
