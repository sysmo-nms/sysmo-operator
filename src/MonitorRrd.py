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

class RrdView(QLabel):
    def __init__(self, parent, probeDict):
        super(RrdView, self).__init__(parent)
        self.setStyleSheet("QFrame { background: #999999 }")
        self.setMinimumWidth(600)
        self.knownHeight    = 0
        self.knownWidth     = 0
        self.probeDict      = probeDict
        self.hexaPalette    = Monitor.MonitorMain.singleton.rgbaDict
        self.needRedraw     = False
        self.rrdfileReady   = False

        # tmp rrd file
        self.rrdDbFile      = QTemporaryFile()
        self.rrdDbFile.open()
        self.rrdDbFile.close()
        self.rrdDbFileName  = self.rrdDbFile.fileName()

        # tmp png file
        self.rrdGraphFile       = QTemporaryFile()
        self.rrdGraphFile.open()
        self.rrdGraphFile.close()
        self.rrdGraphFileName   = self.rrdGraphFile.fileName()

        # rrd conf
        self.rrdUpdateString = self.probeDict['loggers']['btracker_logger_rrd']['update']
        self.rrdMacroBinds   = self.probeDict['loggers']['btracker_logger_rrd']['binds']
        self.rrdGraphConf    = self.probeDict['loggers']['btracker_logger_rrd']['graphs']

    def resizeEvent(self, event):
        if self.rrdfileReady == True: self.needRedraw = True
        QLabel.resizeEvent(self, event)

    def paintEvent(self, event):
        if self.needRedraw == True:
            self.updateGraph()
            self.needRedraw = False
        QLabel.paintEvent(self, event)

    def rrdDump(self, fileName):
        self.rrdfileReady = True
        self.rrdFileName  = fileName
        self.rrdGraphConf = re.sub('<FILE>', self.rrdFileName, self.rrdGraphConf[0])
        self.updateGraph()

    def updateGraph(self):
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
