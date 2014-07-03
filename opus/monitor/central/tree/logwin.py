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

def openLoggerFor(probe, display):
    if probe not in LoggerView.Elements.keys():
        v = LoggerView(probe, display)
        LoggerView.Elements[probe] = v
    else:
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

        scrollArea  = RrdArea(self, probe)

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


class RrdArea(NFrameContainer):
    def __init__(self, parent, probe):
        super(RrdArea, self).__init__(parent)
        self._rrdFrame = RrdLog(self, probe, parent)
        rrdScroll = QScrollArea(self)
        rrdScroll.setWidget(self._rrdFrame)
        rrdScroll.setWidgetResizable(True)

        rrdControls = RrdControls(self)
        grid = NGridContainer(self)
        grid.setVerticalSpacing(4)
        grid.addWidget(rrdControls,          0,0)
        grid.addWidget(rrdScroll,            1,0)
        self.setLayout(grid)

    def timelineMove(self, start, end):
        self._rrdFrame.setTimeline(start, end)

    def heightMove(self, size):
        self._rrdFrame.setGraphHeight(size)

class RrdControls(NFrameContainer):
    def __init__(self, parent):
        super(RrdControls, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(20)
        grid.setContentsMargins(20,0,20,0)
        lo   = RrdLocateControl(self)
        tl   = RrdTimelineControl(self, parent)
        rh   = RrdHeightControl(self, parent)
        un   = RrdUnifyControl(self)
        la   = RrdLayoutControl(self)

        grid.addWidget(lo,          0,0)
        grid.addWidget(tl,          0,1)
        grid.addWidget(rh,          0,2)
        grid.addWidget(un,          0,3)
        grid.addWidget(la,          0,4)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,0)
        grid.setColumnStretch(4,0)
        grid.setColumnStretch(5,1)
        self.setLayout(grid)


class RrdLayoutControl(NFrameContainer):
    def __init__(self, parent):
        super(RrdLayoutControl, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(2)
        heightLab = QLabel('Layout:', self)
        height = QComboBox(self)
        height.addItem('1 column')
        height.addItem('2 columns')
        height.addItem('3 columns')
        height.addItem('4 columns')
        grid.addWidget(heightLab,   0,0)
        grid.addWidget(height,      0,1)
        self.setLayout(grid)

class RrdLocateControl(NFrameContainer):
    def __init__(self, parent):
        super(RrdLocateControl, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(2)
        locateOr = QComboBox(self)
        locateOr.addItem('Locate:')
        locateOr.addItem('Filter:')
        line = QLineEdit(self)
        line.setMinimumWidth(150)
        grid.addWidget(locateOr, 0,0)
        grid.addWidget(line,     0,1)
        self.setLayout(grid)

class RrdUnifyControl(NFrameContainer):
    def __init__(self, parent):
        super(RrdUnifyControl, self).__init__(parent)
        grid = NGridContainer(self)
        unify = QCheckBox('Unify Y axis', self)
        grid.addWidget(unify, 0,0)
        self.setLayout(grid)

class RrdHeightControl(NFrameContainer):
    def __init__(self, parent, master):
        super(RrdHeightControl, self).__init__(parent)
        self._master = master
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(2)
        heightLab = QLabel('Graph height:', self)
        height = QComboBox(self)
        height.insertItem(0, 'Thumbnail')
        height.insertItem(1, 'Small')
        height.insertItem(2, 'Normal')
        height.insertItem(3, 'Large')
        height.insertItem(4, 'Huge')
        height.currentIndexChanged[int].connect(self._heightMove)
        grid.addWidget(heightLab,   0,0)
        grid.addWidget(height,      0,1)
        self.setLayout(grid)

    def _heightMove(self, index):
        if index == 0:
            self._master.heightMove('31')
        elif index == 1:
            self._master.heightMove(80)
        elif index == 2:
            self._master.heightMove(100)
        elif index == 3:
            self._master.heightMove(130)
        elif index == 4:
            self._master.heightMove(180)



class RrdTimelineControl(NFrameContainer):
    def __init__(self, parent, master):
        super(RrdTimelineControl, self).__init__(parent)
        self._master = master
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(2)
        timeLineLab = QLabel('Timeline:', self)
        timeLine = QComboBox(self)
        timeLine.insertItem(0, '2h  from now')
        timeLine.insertItem(1, '12h from now')
        timeLine.insertItem(2, '2d  from now')
        timeLine.insertItem(3, '7d  from now')
        timeLine.insertItem(4, '2w  from now')
        timeLine.insertItem(5, '1m  from now')
        timeLine.insertItem(6, '6m  from now')
        timeLine.insertItem(7, '1y  from now')
        timeLine.insertItem(8, '3y  from now')
        timeLine.insertItem(9, '10y from now')
        timeLine.currentIndexChanged[int].connect(self._timelineMove)
        grid.addWidget(timeLineLab, 0,0)
        grid.addWidget(timeLine,    0,1)
        self.setLayout(grid)

    def _timelineMove(self, index):
        if index == 0:
            start   = 'now-2hours'
            end     = 'now'
            self._master.timelineMove(start, end)
        if index == 1:
            start   = 'now-12hours'
            end     = 'now'
            self._master.timelineMove(start, end)
        elif index == 2:
            end     = 'now'
            start   = 'now-2days'
            self._master.timelineMove(start, end)
        elif index == 3:
            end     = 'now'
            start   = 'now-7days'
            self._master.timelineMove(start, end)
        elif index == 4:
            end     = 'now'
            start   = 'now-2weeks'
            self._master.timelineMove(start, end)
        elif index == 5:
            end     = 'now'
            start   = 'now-1month'
            self._master.timelineMove(start, end)
        elif index == 6:
            end     = 'now'
            start   = 'now-6months'
            self._master.timelineMove(start, end)
        elif index == 7:
            end     = 'now'
            start   = 'now-1year'
            self._master.timelineMove(start, end)
        elif index == 8:
            end     = 'now'
            start   = 'now-3years'
            self._master.timelineMove(start, end)
        elif index == 9:
            end     = 'now'
            start   = 'now-10years'
            self._master.timelineMove(start, end)




class RrdLog(AbstractChannelWidget):
    sizeMove = Signal(int)
    timeMove = Signal(tuple)
    def __init__(self, parent, probe, master):
        super(RrdLog, self).__init__(parent, probe)
        self._master = master
        # XXX try NGrid() in a QThred()
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
                self._master.updateProgress(fileId)
        elif msg['msgType'] == 'probeReturn':
            for key in self._rrdElements.keys():
                self._rrdElements[key].handleReturn(msg)

class RrdElement(QLabel):
    def __init__(self, parent, rrdname, rrdconf):
        super(RrdElement, self).__init__(parent)
        self.setMinimumWidth(400)

        self._resizeTimeline = QTimeLine(100, self)
        self._resizeTimeline.setUpdateInterval(1000)
        self._resizeTimeline.setCurveShape(QTimeLine.LinearCurve)
        self._resizeTimeline.finished.connect(self._resizeEventEnd)

        parent.sizeMove.connect(self.setHeight,     Qt.QueuedConnection)
        parent.timeMove.connect(self.setTimeline,   Qt.QueuedConnection)

        self._font = QFont().defaultFamily()
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
            self._sizeOrigin = event.size().width()
            self._resizeTimeline.start()
        else:
            self._resizeTimeline.setCurrentTime(0)

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
        #print "update graph"
        # TODO use re.compile and re.match or re.search using MatchObject
        defs    = re.findall(r'DEF:[^\s]+', self._rrdgraphcmd)
        lines   = re.findall(r'LINE[^\s]+', self._rrdgraphcmd)
        areas   = re.findall(r'AREA[^\s]+', self._rrdgraphcmd)
        size    = self.size()
        rrdwidth    = size.width()
        #rrdheight   = size.height()
        height      = self._graphHeight
        start       = self._timelineStart
        end         = self._timelineEnd
        #cmd         = self._generateGraphCmd(
        #    start, end, defs, lines, areas, rrdwidth, rrdheight)
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
        print "stateupdate: ", self, self._needRedraw, self._rrdFileReady
        if self._needRedraw == True:
            if self._rrdFileReady == True:
                self._updateGraph()
                self._needRedraw = False



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

        cmd = '%s%s%s%s%s%s%s%s' % (head, time, opts, colors, time, defsC, linesC, areasC)
        return cmd

    def _generateThumbCmd(self, rrdStart, rrdStop, defs, lines, areas, w, h):
        head = 'graph %s --imgformat PNG --width %s --height %s --border 0 ' % (self._rrdGraphFile, w, h)
        opts = '--only-graph --disable-rrdtool-tag --slope-mode --tabwidth 1 '
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

        cmd = '%s%s%s%s%s%s%s%s' % (head, time, opts, colors, time, defsC, linesC, areasC)
        return cmd
