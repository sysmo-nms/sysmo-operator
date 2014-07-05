from    PySide.QtCore   import (
    QTemporaryFile,
    QSettings,
    QSize,
    QTimeLine,
    Signal,
    Qt
)

from    PySide.QtGui    import (
    QWidget,
    QDialog,
    QScrollArea,
    QPixmap,
    QPalette,
    QFont,
    QStatusBar,
    QProgressBar,
    QPushButton,
    QComboBox,
    QCheckBox,
    QLineEdit
)

from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid,
    QLabel
)

from    opus.monitor.proxy  import AbstractChannelWidget
import  opus.monitor.api    as monapi
import  opus.monitor.norrd  as norrd
import  nocapi
import  platform
import  re

class RrdLog(AbstractChannelWidget):
    sizeMove = Signal(int)
    timeMove = Signal(tuple)
    def __init__(self, parent, probe, master):
        super(RrdLog, self).__init__(parent, probe)
        self._master = master
        self._grid = NGrid(self)
        self.setLayout(self._grid)
        self._rrdElements = dict()

        self.probeName  = probe
        probes          = monapi.getProbesDict()
        self._probeConf = probes[probe]

        if 'bmonitor_logger_rrd' in self._probeConf['loggers'].keys():
            self._continue()
        else:
            self._cancel()

    def setTimeline(self, start, end):
        self.timeMove.emit((start,end))

    def setGraphHeight(self, size):
        self.sizeMove.emit(size)

    def _continue(self):
        rrdConf = self._probeConf['loggers']['bmonitor_logger_rrd']
        self._master.setProgressMax(len(rrdConf.keys()))
        for rrdname in rrdConf.keys():
            rrdconf = rrdConf[rrdname]
            self._rrdElements[rrdname] = RrdGraph(self, rrdname, rrdconf)
            self._grid.addWidget(self._rrdElements[rrdname])
            rcount = self._grid.rowCount()
            self._grid.setRowStretch(rcount - 1, 0)
            self._grid.setRowStretch(rcount,     1)
        self.connectProbe()
        self.goOn = True

    def _cancel(self):
        self.goOn = False

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'bmonitor_logger_rrd':
                fileId      = msg['data']['fileId']
                fileName    = msg['data']['file']
                self._rrdElements[fileId].handleDump(fileName)
                self._master.updateProgress(fileId)
        elif msg['msgType'] == 'probeReturn':
            for key in self._rrdElements.keys():
                self._rrdElements[key].handleReturn(msg)

class RrdGraph(QLabel):
    def __init__(self, parent, rrdname, rrdconf):
        super(RrdGraph, self).__init__(parent)
        self.setMinimumWidth(400)

        self._resizeTimeline = QTimeLine(100, self)
        self._resizeTimeline.setCurveShape(QTimeLine.LinearCurve)
        self._resizeTimeline.finished.connect(self._resizeEventEnd)

        parent.sizeMove.connect(self.setHeight,     Qt.QueuedConnection)
        parent.timeMove.connect(self.setTimeline,   Qt.QueuedConnection)

        self._initGraphFile()
        self.setText(rrdname)
        self._rrdname       = rrdname
        self._rrdconf       = rrdconf
        # XXX 
        #print rrdconf['graphs']
        rrdgraphcmd         = rrdconf['graphs'][0]
        # XXX 
        self._rrdgraphcmd   = rrdgraphcmd
        self._rrdgraphbinds = rrdconf['binds']

        self._rrdFileReady  = False
        self._needRedraw    = True

        # 
        self._timelineStart = 'now-2h'
        self._timelineEnd   = 'now'
        self._graphHeight   = 100

        self._colorBase         = nocapi.nGetRgba('Base')
        self._colorDark         = nocapi.nGetRgba('Dark')
        self._colorShadow       = nocapi.nGetRgba('Shadow')
        self._colorWindowText   = nocapi.nGetRgba('WindowText')
        self._colorWindow       = nocapi.nGetRgba('Window')
        self._font = QFont().defaultFamily()

    def handleReturn(self, msg):
        if self.isVisible() == True: self._updateGraph()

    def handleDump(self, fileName):
        self._rrdDatabase = fileName
        graphcmd = self._rrdgraphcmd
        self._rrdgraphcmd   = re.sub('<FILE>',self._rrdDatabase,graphcmd)
        self._rrdFileReady  = True
        self._stateUpdate()

    def resizeEvent(self, event):
        if self._resizeTimeline.state() == QTimeLine.NotRunning:
            self._sizeOrigin = event.oldSize().width()
            self._resizeTimeline.start()
        else:
            self._resizeTimeline.setCurrentTime(0)
        QLabel.resizeEvent(self, event)

    def _resizeEventEnd(self):
        if self.size().width() != self._sizeOrigin:
            self._needRedraw = True
            self._stateUpdate()

    def setTimeline(self, time):
        start, end = time
        self._timelineStart = start
        self._timelineEnd   = end
        self._needRedraw = True
        self._stateUpdate()

    def setHeight(self, size):
        self._graphHeight = size
        self._needRedraw = True
        self._stateUpdate()

    def _updateRequired(self):
        self._needRedraw = True
        self._stateUpdate()


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
        defs    = re.findall(r'DEF:[^\s]+', self._rrdgraphcmd)
        lines   = re.findall(r'LINE[^\s]+', self._rrdgraphcmd)
        areas   = re.findall(r'AREA[^\s]+', self._rrdgraphcmd)
        size    = self.size()
        rrdwidth    = size.width()
        height      = self._graphHeight
        start       = self._timelineStart
        end         = self._timelineEnd
        if int(height) < 32:
            cmd = self._generateThumbCmd(
                start, end, defs, lines, areas, rrdwidth, height)
        else:
            cmd = self._generateGraphCmd(
                start, end, defs, lines, areas, rrdwidth, height)
        norrd.cmd(cmd, callback=self._drawGraph, special='returnPixmap', data=self._rrdGraphFile)

    def _drawGraph(self, rrdreturn):
        pix = rrdreturn['data']
        self.setPixmap(pix)


    def _stateUpdate(self):
        #print "stateupdate: ", self, self._needRedraw, self._rrdFileReady
        if self._needRedraw == True:
            if self._rrdFileReady == True:
                self._updateGraph()
                self._needRedraw = False



    def _generateGraphCmd(self, rrdStart, rrdStop, defs, lines, areas, w, h):
        head    = 'graph %s --imgformat PNG --width %s --height %s --border 0 ' % (self._rrdGraphFile, w, h)
        opts    = '--full-size-mode --disable-rrdtool-tag --slope-mode --tabwidth 1 -W %s ' % self._rrdname
        colors  = '--color BACK#00000000 --color CANVAS%s --color GRID%s --color MGRID%s --color FONT%s --color AXIS%s --color FRAME%s --color ARROW%s --font DEFAULT:0:%s ' % (
                self._colorBase,
                self._colorDark,
                self._colorShadow,
                self._colorWindowText,
                self._colorDark,
                self._colorWindow,
                self._colorShadow,
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

        cmd = '%s%s%s%s%s%s%s%s' % (head, time, opts, colors, time, defsC, linesC, areasC)
        return cmd

    def _generateThumbCmd(self, rrdStart, rrdStop, defs, lines, areas, w, h):
        head = 'graph %s --imgformat PNG --width %s --height %s --border 0 ' % (self._rrdGraphFile, w, h)
        opts = '--only-graph --disable-rrdtool-tag --slope-mode --tabwidth 1 '
        colors = '--color BACK#00000000 --color CANVAS%s --color GRID%s --color MGRID%s --color FONT%s --color AXIS%s --color FRAME%s --color ARROW%s --font DEFAULT:0:%s ' % (
                self._colorBase,
                self._colorDark,
                self._colorShadow,
                self._colorWindowText,
                self._colorDark,
                self._colorWindow,
                self._colorShadow,
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

        cmd = '%s%s%s%s%s%s%s%s' % (head, time, opts, colors, time, defsC, linesC, areasC)
        return cmd
