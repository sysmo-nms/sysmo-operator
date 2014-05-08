from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    QLabel
)
from    PySide.QtCore   import QTemporaryFile
from    PySide.QtGui    import QPixmap, QPalette, QFont
from    opus.monitor.dash_area.dash_widgets import DashTreeWidget
from    opus.monitor.proxy  import AbstractChannelWidget
import  opus.monitor.api    as monapi
import  opus.monitor.norrd  as norrd
import  nocapi
import  platform
import  re

class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        dashWidget = DashTreeWidget(self)
        dashWidget.setDashLabels('Elements', 'RRDs logs')
        dashWidget.setItemWidgetClass(RrdLog)
        self._grid.addWidget(dashWidget, 0,0)
        self.setLayout(self._grid)

class RrdLog(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdLog, self).__init__(parent, probe)
        self._grid = NGridContainer(self)
        self.setLayout(self._grid)
        self._rrdElements = dict()

        self.probeName  = probe
        probes          = monapi.getProbesDict()
        self._probeConf = probes[probe]

        if 'bmonitor_logger_rrd' in self._probeConf['loggers'].keys():
            self._continue()
        else:
            self._cancel()

    def _continue(self):
        rrdConf = self._probeConf['loggers']['bmonitor_logger_rrd']
        for rrdname in rrdConf.keys():
            rrdconf = rrdConf[rrdname]
            self._rrdElements[rrdname] = RrdElement(self, rrdname, rrdconf)
            self._grid.addWidget(self._rrdElements[rrdname])
        self.connectProbe()
        self.goOn = True

    def _cancel(self):
        self.goOn = False

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'bmonitor_logger_rrd':
                for key in self._rrdElements.keys():
                    self._rrdElements[key].handleDump(msg)
        elif msg['msgType'] == 'probeReturn':
            for key in self._rrdElements.keys():
                self._rrdElements[key].handleReturn(msg)

class RrdElement(QLabel):
    def __init__(self, parent, rrdname, rrdconf):
        super(RrdElement, self).__init__(parent)
        self._font = QFont().defaultFamily()
        self._initGraphState()
        self._initGraphFile()
        self.setText(rrdname)
        self._rrdname       = rrdname
        self._rrdconf       = rrdconf
        [rrdgraphcmd]       = rrdconf['graphs']
        self._rrdgraphcmd   = rrdgraphcmd
        self._rrdgraphbinds = rrdconf['binds']
        self.setFixedHeight(100)

    def _initGraphState(self):
        self._rrdFileReady  = False
        self._needRedraw    = False
        self._needRegraph   = False

    def _initGraphFile(self):
        self._rrdGraphFile  = QTemporaryFile(self)
        self._rrdGraphFile.open()
        self._rrdGraphFile.close()
        filename            = self._rrdGraphFile.fileName()
        if platform.system() == 'Windows':
            winfileName = filename.replace("/","\\\\").replace(":", "\\:")
            self._rrdGraphFile = winfileName
            self._rrdFileReady = True
        else:
            self._rrdGraphFile = filename
            self._rrdFileReady = True

    def _updateGraph(self):
        #print "update graph"
        # TODO use re.compile and re.match or re.search using MatchObject
        defs    = re.findall(r'DEF:[^\s]+', self._rrdgraphcmd)
        lines   = re.findall(r'LINE[^\s]+', self._rrdgraphcmd)
        areas   = re.findall(r'AREA[^\s]+', self._rrdgraphcmd)
        size    = self.size()
        rrdwidth    = size.width()
        rrdheight   = size.height()
        cmd         = self._generateGraphCmd(
            'now-3600s', 'now', defs, lines, areas, rrdwidth, rrdheight)
        norrd.cmd(cmd, self._drawGraph)

    #def _graphComplete(self, rrdreturn):
        #self._needRedraw = True
        #if self.isVisible() == True:
            #self._drawGraph()

    def showEvent(self, event):
        print "show event"

    def _drawGraph(self, rrdreturn):
        self.setPixmap(QPixmap(self._rrdGraphFile))

    #def resizeEvent(self, event):
        #if self._rrdFileReady == True:
            #self._needRedraw = True
        #QLabel.resizeEvent(self, event)

    #def paintEvent(self, event):
        #if self._needRedraw == True:
        #self._updateGraph()
        #QLabel.paintEvent(self, event)

    def handleDump(self, msg):
        self._rrdDatabase = msg['data'][self._rrdname]
        graphcmd = self._rrdgraphcmd
        self._rrdgraphcmd   = re.sub('<FILE>',self._rrdDatabase,graphcmd)
        self._rrdFileReady  = True

    def handleReturn(self, msg):
        if self.isVisible() == True: self._updateGraph()

    def _generateGraphCmd(self, rrdStart, rrdStop, defs, lines, areas, w, h):
        head = 'graph %s --imgformat PNG --width %s --height %s --border 0 ' % (self._rrdGraphFile, w, h)
        #opts = '--full-size-mode --disable-rrdtool-tag --slope-mode --tabwidth 40 --watermark %s' % 'watermark '
        opts = '--full-size-mode --disable-rrdtool-tag --slope-mode --tabwidth 1 -W %s ' % self._rrdname
        #opts = '--full-size-mode --disable-rrdtool-tag --border 0 --dynamic-labels --slope-mode --tabwidth 40 --watermark %s' % 'watermark '


        colors = '--color BACK#00000000 --color CANVAS%s --color GRID%s --color MGRID%s --color FONT%s --color AXIS%s --color FRAME%s --color ARROW%s --font DEFAULT:0:%s ' % (
                nocapi.nGetRgba('Base'),
                nocapi.nGetRgba('Dark'),
                nocapi.nGetRgba('Shadow'),
                nocapi.nGetRgba('WindowText'),
                nocapi.nGetRgba('Dark'),
                nocapi.nGetRgba('Window'),
                nocapi.nGetRgba('Shadow'),
                self._font
            )
        time = '--start %s --end %s ' % (rrdStart, rrdStop)
        defsC = ''
        for i in range(len(defs)):
            defsC += ' %s ' % defs[i]

        linesC = ''
        for i in range(len(lines)):
            linesC += ' %s ' % lines[i]

        areasC = ''
        for i in range(len(areas)):
            areasC += ' %s ' % areas[i]

        cmd = head + time + opts + colors + time + defsC + linesC + areasC
        return cmd
