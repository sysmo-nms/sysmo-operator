
from    PySide.QtCore   import (
    QTemporaryFile,
    QSettings,
    QSize,
    QTimeLine
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
    QPushButton
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

def openLoggerFor(probe, display):
    if probe not in LoggerView.Elements.keys():
        #p = opus.monitor.main.Central.singleton
        v = LoggerView(probe, display)
        LoggerView.Elements[probe] = v
    else:
        print "exists !!"
        LoggerView.Elements[probe].show()
    
class LoggerView(QDialog):
    Elements = dict()
    def __init__(self, probe, display, parent=None):
        super(LoggerView, self).__init__(parent)
        nocapi.nConnectWillClose(self._willClose)
        self._element = probe
        self.setWindowTitle(display)

        self._statusBar = LogStatusBar(self)

        menus       = ProbeMenus(self)

        scrollArea  = QScrollArea(self)
        scrollArea.setWidget(RrdLog(self, probe))
        scrollArea.setWidgetResizable(True)

        grid = NGrid(self)
        grid.addWidget(scrollArea, 0,1)
        grid.addWidget(menus,      0,0)
        grid.addWidget(self._statusBar,  1,0,1,2)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,0)

        self.setLayout(grid)
        self.show()

    def setProgressMax(self, maxi):
        self._statusBar.progress.setMaximum(maxi)

    def updateProgress(self, fileId):
        self._statusBar.updateProgress(fileId)

    def _restoreSettings(self):
        settings = QSettings()
        settingsString = 'monitor/element_perf_geometry/%s' % self._element
        geometry = settings.value(settingsString)
        if geometry != None:
            self.restoreGeometry(geometry)

    def _saveSettings(self):
        settings = QSettings()
        settingsString = 'monitor/element_perf_geometry/%s' % self._element
        settings.setValue(settingsString, self.saveGeometry())

    def _willClose(self):
        self._saveSettings()
        self.close()

    def show(self):
        self._restoreSettings()
        self.raise_()
        QDialog.show(self)

    def closeEvent(self, event):
        self._saveSettings()
        QDialog.closeEvent(self, event)

class ProbeMenus(NFrameContainer):
    def __init__(self, parent):
        super(ProbeMenus, self).__init__(parent)
        self._force = QPushButton(self)
        self._force.setIconSize(QSize(30,30))
        self._force.setIcon(nocapi.nGetIcon('software-update-available'))
        self._pause = QPushButton(self)
        self._pause.setIconSize(QSize(30,30))
        self._pause.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self._pause.setCheckable(True)
        self._pause.setChecked(False)
        self._action = QPushButton(self)
        self._action.setIconSize(QSize(30,30))
        self._action.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self._docu = QPushButton(self)
        self._docu.setIconSize(QSize(30,30))
        self._docu.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self._prop = QPushButton(self)
        self._prop.setIconSize(QSize(30,30))
        self._prop.setIcon(nocapi.nGetIcon('edit-paste'))

        grid = NGridContainer(self)
        grid.setVerticalSpacing(4)
        grid.addWidget(self._force, 0,1,1,1)
        grid.addWidget(self._pause, 1,1)
        grid.addWidget(self._action, 2,1)
        grid.addWidget(self._docu,  4,1)
        grid.addWidget(self._prop,  5,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,0)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,0)
        grid.setRowStretch(5,0)
        self.setLayout(grid)


class LogStatusBar(QStatusBar):
    def __init__(self, parent):
        super(LogStatusBar, self).__init__(parent)
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        self.addPermanentWidget(self.progress)

    def updateProgress(self, info):
        val = self.progress.value()
        self.progress.setValue(val + 1)
        self.progress.setFormat('Loading data: %p%')
        self.showMessage('Loading RRD file for If %s' % info)
        if self.progress.maximum() == val + 1:
            self.removeWidget(self.progress)
            self.showMessage('Load complete', timeout=2000)

class RrdLog(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdLog, self).__init__(parent, probe)
        self._resizeTimeline = QTimeLine(50, self)
        self._resizeTimeline.setUpdateInterval(100)
        self._resizeTimeline.setCurveShape(QTimeLine.LinearCurve)
        self._resizeTimeline.finished.connect(self._updateGraphs)

        self._parent = parent
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

    def resizeEvent(self, event):
        if self._resizeTimeline.state() == QTimeLine.NotRunning:
            self._resizeTimeline.start()
        else:
            self._resizeTimeline.setCurrentTime(0)

    def _updateGraphs(self):
        for key in self._rrdElements.keys():
            self._rrdElements[key].resizeEnding()

    def _continue(self):
        rrdConf = self._probeConf['loggers']['bmonitor_logger_rrd']
        self._parent.setProgressMax(len(rrdConf.keys()))
        for rrdname in rrdConf.keys():
            rrdconf = rrdConf[rrdname]
            self._rrdElements[rrdname] = RrdElement(self, rrdname, rrdconf)
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
                self._parent.updateProgress(fileId)
        elif msg['msgType'] == 'probeReturn':
            for key in self._rrdElements.keys():
                self._rrdElements[key].handleReturn(msg)

class RrdElement(QLabel):
    def __init__(self, parent, rrdname, rrdconf):
        super(RrdElement, self).__init__(parent)
        self.setMinimumWidth(400)
        self.setMinimumHeight(100)
        self._font = QFont().defaultFamily()
        self._initGraphState()
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

    def resizeEnding(self):
        self._updateGraph()

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
            'now-2h', 'now', defs, lines, areas, rrdwidth, rrdheight)
        norrd.cmd(cmd, self._drawGraph)

    #def _graphComplete(self, rrdreturn):
        #self._needRedraw = True
        #if self.isVisible() == True:
            #self._drawGraph()

    def showEvent(self, event):
        print "show event"

    def _drawGraph(self, rrdreturn):
        self.setPixmap(QPixmap(self._rrdGraphFile))

#    def resizeEvent(self, event):
#        print "resize event"
        #if self._rrdFileReady == True:
            #self._needRedraw = True
        #QLabel.resizeEvent(self, event)

    #def paintEvent(self, event):
        #if self._needRedraw == True:
        #self._updateGraph()
        #QLabel.paintEvent(self, event)

    def handleDump(self, fileName):
        self._rrdDatabase = fileName
        graphcmd = self._rrdgraphcmd
        self._rrdgraphcmd   = re.sub('<FILE>',self._rrdDatabase,graphcmd)
        self._rrdFileReady  = True
        self._updateGraph()

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
