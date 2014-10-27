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
    QLineEdit,
    QTabWidget
)

from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid,
    QLabel
)

from    opus.monitor.proxy  import AbstractChannelWidget, ChanHandler
import  opus.monitor.api    as monapi
import  opus.monitor.norrd  as norrd
import  nocapi

import  nocapi
import  platform
import  re


class RrdArea(NFrameContainer):
    def __init__(self, parent, probe):
        super(RrdArea, self).__init__(parent)
        self._rrdFrame = RrdFrame(self, probe)
        self._rrdScroll = QScrollArea(self)
        self._rrdScroll.setMinimumWidth(400)
        self._rrdScroll.setMinimumHeight(200)
        self._rrdScroll.setWidget(self._rrdFrame)
        self._rrdScroll.setWidgetResizable(True)

        rrdControls = RrdControls(self)
        grid = NGrid(self)
        grid.setVerticalSpacing(4)
        grid.addWidget(rrdControls,     0,0)
        grid.addWidget(self._rrdScroll, 0,1)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        self.setLayout(grid)

class RrdFrame(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdFrame, self).__init__(parent, probe)

        self._layout = NGrid(self)
        self._graphElements = dict()
        self._probeName = probe
        self._probeConf = monapi.getProbesDict()[probe]
        rrdConf = self._probeConf['loggers']['bmonitor_logger_rrd']
        for i in range(len(rrdConf['indexes'])):
            index = rrdConf['indexes'][i]
            self._graphElements[index] = RrdGraphArea(self, index, rrdConf['rgraphs'])
            self._layout.addWidget(self._graphElements[index], i, 0)
            self._layout.setRowStretch(i, 0)

        self._layout.setRowStretch(len(rrdConf['indexes']), 1)
        self.connectProbe()

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'rrdProbeEvent':
            index = msg['data']
            self._graphElements[index].rrdUpdateEvent()
        elif msg['msgType'] == 'probeDump':
            if msg['logger'] == 'bmonitor_logger_rrd2':
                (index, rrdDbFile) = msg['data']
                self._graphElements[index].setRrdDbFile(rrdDbFile)

class RrdGraphArea(NFrameContainer):
    def __init__(self, parent, index, graphConf):
        super(RrdGraphArea, self).__init__(parent)
        self._layout    = NGridContainer(self)
        self._graphs    = dict()
        self._index     = index
        self._graphConf = graphConf
        for gindex in graphConf.keys():
            self._graphs[gindex] = RrdGraph(self, graphConf[gindex])
            self._layout.addWidget(self._graphs[gindex], 0,gindex)

    def setRrdDbFile(self, fileName):
        for key in self._graphs.keys():
            self._graphs[key].setRrdDbFile(fileName)
        self.rrdUpdateEvent()

    def rrdUpdateEvent(self):
        for key in self._graphs.keys():
            self._graphs[key].rrdUpdateEvent()


class RrdGraph(QLabel):
    def __init__(self, parent, graphConf):
        super(RrdGraph, self).__init__(parent)
        self._rrdGraphFile  = QTemporaryFile(self)
        self._rrdGraphFile.open()
        self._rrdGraphFile.close()
        self._rrdGraphFileName = self._rrdGraphFile.fileName()
        self._rrdPixmap = QPixmap()
        self.setPixmap(self._rrdPixmap)
        #if platform.system() == 'Windows':
            #winfileName = filename.replace("/","\\\\").replace(":", "\\:")
            #self._rrdGraphFile = winfileName
        #else:
            #self._rrdGraphFile = filename

        self._rrdDbFileName = None
        self._rrdGraphOpts  = None
        self._rrdGraph      = graphConf

    def setRrdDbFile(self, fileName):
        self._rrdDbFileName = fileName
        self._rrdGraphOpts = '\
--border 0 \
--full-size-mode \
--disable-rrdtool-tag \
--slope-mode \
--tabwidth 1 \
--color BACK#00000000 \
--color CANVAS%s \
--color GRID%s \
--color MGRID%s \
--color FONT%s \
--color AXIS%s \
--color FRAME%s \
--color ARROW%s \
--font DEFAULT:0:%s ' % (
                nocapi.nGetRgba('Base'),
                nocapi.nGetRgba('Dark'),
                nocapi.nGetRgba('Shadow'),
                nocapi.nGetRgba('WindowText'),
                nocapi.nGetRgba('Dark'),
                nocapi.nGetRgba('Window'),
                nocapi.nGetRgba('Shadow'),
                QFont().defaultFamily()
            )
        self._rrdGraph = re.sub('<FILE>', self._rrdDbFileName, self._rrdGraph)

    def rrdUpdateEvent(self):
        cmd = self._generateGraphCmd()
        norrd.cmd(
            cmd,
            callback=self._rrdUpdateReply,
            data=self._rrdGraphFileName)

    def _rrdUpdateReply(self, rrdreply):
        self._rrdPixmap.load(self._rrdGraphFileName)
        self.setPixmap(self._rrdPixmap)

    def _generateGraphCmd(self):
        return "graph %s %s %s" % (
            self._rrdGraphFileName,
            self._rrdGraphOpts,
            self._rrdGraph)

class RrdControls(NFrameContainer):
    def __init__(self, parent):
        super(RrdControls, self).__init__(parent)
        self._layout = NGridContainer(self)
        self._layout.setRowStretch(10, 1)

        self._locateLabel   = QLabel('Search:', self)
        self._locateCtrl    = QLineEdit(self)
        self._layout.addWidget(self._locateLabel, 0,0)
        self._layout.addWidget(self._locateCtrl,  0,1)
        self._layout.setRowStretch(0,0)

        self._timeLineLabel = QLabel('Timeline:', self)
        self._timeLineCtrl = QComboBox(self)
        self._timeLineCtrl.insertItem(0, '2h  from now')
        self._timeLineCtrl.insertItem(1, '12h from now')
        self._timeLineCtrl.insertItem(2, '2d  from now')
        self._timeLineCtrl.insertItem(3, '7d  from now')
        self._timeLineCtrl.insertItem(4, '2w  from now')
        self._timeLineCtrl.insertItem(5, '1m  from now')
        self._timeLineCtrl.insertItem(6, '6m  from now')
        self._timeLineCtrl.insertItem(7, '1y  from now')
        self._timeLineCtrl.insertItem(8, '3y  from now')
        self._timeLineCtrl.insertItem(9, '10y from now')
        self._layout.addWidget(self._timeLineLabel, 1,0)
        self._layout.addWidget(self._timeLineCtrl,  1,1)
        self._layout.setRowStretch(1,0)

        self._heightLabel = QLabel('Graph height:', self)
        self._heightCtrl = QComboBox(self)
        self._heightCtrl.insertItem(0, 'Thumbnail')
        self._heightCtrl.insertItem(1, 'Small')
        self._heightCtrl.insertItem(2, 'Normal')
        self._heightCtrl.insertItem(3, 'Large')
        self._heightCtrl.insertItem(4, 'Huge')
        self._layout.addWidget(self._heightLabel, 2,0)
        self._layout.addWidget(self._heightCtrl,  2,1)
        self._layout.setRowStretch(2,0)
 
        self._layoutLabel = QLabel('Layout:', self)
        self._layoutCtrl = QComboBox(self)
        self._layoutCtrl.addItem('1 column')
        self._layoutCtrl.addItem('2 columns')
        self._layoutCtrl.addItem('3 columns')
        self._layoutCtrl.addItem('4 columns')
        self._layout.addWidget(self._layoutLabel, 3,0)
        self._layout.addWidget(self._layoutCtrl,  3,1)
        self._layout.setRowStretch(3,0)
 
        self._unifyLabel = QLabel('Unify Y axis:', self)
        self._unifyCtrl  = QCheckBox(self)
        self._layout.addWidget(self._unifyLabel, 4,0)
        self._layout.addWidget(self._unifyCtrl,  4,1)
        self._layout.setRowStretch(4,0)



 



# class RrdControls2(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdControls2, self).__init__(parent)
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(20)
#         grid.setContentsMargins(20,0,20,0)
#         lo   = RrdLocateControl(self)
#         tl   = RrdTimelineControl(self, parent)
#         rh   = RrdHeightControl(self, parent)
#         un   = RrdUnifyControl(self)
#         la   = RrdLayoutControl(self)
# 
#         #
#         lo.setDisabled(True)
#         un.setDisabled(True)
#         la.setDisabled(True)
#         #
#         grid.addWidget(lo,          0,0)
#         grid.addWidget(tl,          0,1)
#         grid.addWidget(rh,          0,2)
#         grid.addWidget(un,          0,3)
#         grid.addWidget(la,          0,4)
#         grid.setColumnStretch(0,0)
#         grid.setColumnStretch(1,0)
#         grid.setColumnStretch(2,0)
#         grid.setColumnStretch(3,0)
#         grid.setColumnStretch(4,0)
#         grid.setColumnStretch(5,1)
#         self.setLayout(grid)
# 
# 
# class RrdLayoutControl(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdLayoutControl, self).__init__(parent)
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         heightLab = QLabel('Layout:', self)
#         height = QComboBox(self)
#         height.addItem('1 column')
#         height.addItem('2 columns')
#         height.addItem('3 columns')
#         height.addItem('4 columns')
#         grid.addWidget(heightLab,   0,0)
#         grid.addWidget(height,      0,1)
#         self.setLayout(grid)
# 
# class RrdLocateControl(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdLocateControl, self).__init__(parent)
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         locateOr = QComboBox(self)
#         locateOr.addItem('Locate:')
#         locateOr.addItem('Filter:')
#         line = QLineEdit(self)
#         line.setMinimumWidth(150)
#         grid.addWidget(locateOr, 0,0)
#         grid.addWidget(line,     0,1)
#         self.setLayout(grid)
# 
# class RrdUnifyControl(NFrameContainer):
#     def __init__(self, parent):
#         super(RrdUnifyControl, self).__init__(parent)
#         grid = NGridContainer(self)
#         unify = QCheckBox('Unify Y axis', self)
#         grid.addWidget(unify, 0,0)
#         self.setLayout(grid)
# 
# class RrdHeightControl(NFrameContainer):
#     def __init__(self, parent, master):
#         super(RrdHeightControl, self).__init__(parent)
#         self._master = master
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         heightLab = QLabel('Graph height:', self)
#         height = QComboBox(self)
#         height.insertItem(0, 'Thumbnail')
#         height.insertItem(1, 'Small')
#         height.insertItem(2, 'Normal')
#         height.insertItem(3, 'Large')
#         height.insertItem(4, 'Huge')
#         height.currentIndexChanged[int].connect(self._heightMove)
#         grid.addWidget(heightLab,   0,0)
#         grid.addWidget(height,      0,1)
#         self.setLayout(grid)
# 
#     def _heightMove(self, index):
#         if index == 0:
#             self._master.heightMove(31)
#         elif index == 1:
#             self._master.heightMove(80)
#         elif index == 2:
#             self._master.heightMove(100)
#         elif index == 3:
#             self._master.heightMove(130)
#         elif index == 4:
#             self._master.heightMove(180)
# 
# 
# 
# class RrdTimelineControl(NFrameContainer):
#     def __init__(self, parent, master):
#         super(RrdTimelineControl, self).__init__(parent)
#         self._master = master
#         grid = NGridContainer(self)
#         grid.setHorizontalSpacing(2)
#         timeLineLab = QLabel('Timeline:', self)
#         timeLine = QComboBox(self)
#         timeLine.insertItem(0, '2h  from now')
#         timeLine.insertItem(1, '12h from now')
#         timeLine.insertItem(2, '2d  from now')
#         timeLine.insertItem(3, '7d  from now')
#         timeLine.insertItem(4, '2w  from now')
#         timeLine.insertItem(5, '1m  from now')
#         timeLine.insertItem(6, '6m  from now')
#         timeLine.insertItem(7, '1y  from now')
#         timeLine.insertItem(8, '3y  from now')
#         timeLine.insertItem(9, '10y from now')
#         timeLine.currentIndexChanged[int].connect(self._timelineMove)
#         grid.addWidget(timeLineLab, 0,0)
#         grid.addWidget(timeLine,    0,1)
#         self.setLayout(grid)
# 
#     def _timelineMove(self, index):
#         if index == 0:
#             start   = 'now-2hours'
#             end     = 'now'
#             self._master.timelineMove(start, end)
#         if index == 1:
#             start   = 'now-12hours'
#             end     = 'now'
#             self._master.timelineMove(start, end)
#         elif index == 2:
#             end     = 'now'
#             start   = 'now-2days'
#             self._master.timelineMove(start, end)
#         elif index == 3:
#             end     = 'now'
#             start   = 'now-7days'
#             self._master.timelineMove(start, end)
#         elif index == 4:
#             end     = 'now'
#             start   = 'now-2weeks'
#             self._master.timelineMove(start, end)
#         elif index == 5:
#             end     = 'now'
#             start   = 'now-1month'
#             self._master.timelineMove(start, end)
#         elif index == 6:
#             end     = 'now'
#             start   = 'now-6months'
#             self._master.timelineMove(start, end)
#         elif index == 7:
#             end     = 'now'
#             start   = 'now-1year'
#             self._master.timelineMove(start, end)
#         elif index == 8:
#             end     = 'now'
#             start   = 'now-3years'
#             self._master.timelineMove(start, end)
#         elif index == 9:
#             end     = 'now'
#             start   = 'now-10years'
#             self._master.timelineMove(start, end)

class RrdLog2(AbstractChannelWidget):
    sizeMove = Signal(int)
    timeMove = Signal(tuple)
    def __init__(self, parent, probe, master):
        super(RrdLog2, self).__init__(parent, probe)
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
        print "continue?", self._probeConf['loggers']['bmonitor_logger_rrd'].keys()
        rrdConf = self._probeConf['loggers']['bmonitor_logger_rrd']
        self._master.setProgressMax(len(rrdConf['indexes']))
        gconf = self._probeConf['loggers']['bmonitor_logger_rrd']['rgraphs']
        for index in rrdConf['indexes']:
            print index, gconf
            self._rrdElements[index] = RrdGraph2(self, index, gconf)
            self._grid.addWidget(self._rrdElements[index])
            rcount = self._grid.rowCount()
            self._grid.setRowStretch(rcount - 1, 0)
            self._grid.setRowStretch(rcount,     1)
        self.connectProbe()
        self.goOn = True

    def _cancel(self):
        print "cancel?"
        self.goOn = False

    def handleProbeEvent(self, msg):
        print "probe event: ", msg

    def handleProbeEvent2(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'bmonitor_logger_rrd':
                fileId      = msg['data']['fileId']
                fileName    = msg['data']['file']
                self._rrdElements[fileId].handleDump(fileName)
                self._master.updateProgress(fileId)
        elif msg['msgType'] == 'probeReturn':
            for key in self._rrdElements.keys():
                self._rrdElements[key].handleReturn(msg)

class RrdGraph2(QLabel):
    def __init__(self, parent, rrdname, rrdconf):
        super(RrdGraph2, self).__init__(parent)
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
