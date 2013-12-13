from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    MonitorRrd          import *
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
import  TkorderIcons
import  os
import  datetime

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class WorkView(QFrame):
    def __init__(self, parent):
        super(WorkView, self).__init__(parent)

        self.tmpMainGridCount = 0

        self.probeViews = dict()

        self.mainGrid   = QGridLayout()
        self.mainFrame  = QFrame(self)
        self.mainFrame.setBackgroundRole(QPalette.Base)
        self.mainFrame.setLayout(self.mainGrid)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.mainFrame)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(Controls(self), 0,0)
        grid.addWidget(self.scroll, 1,0)
        self.setLayout(grid)

    def deleteProbeView(self, probe):
        probeView = self.probeViews[probe]
        self.mainGrid.removeWidget(probeView)
        probeView.deleteLater()
        self.mainGrid.update()
        
        del self.probeViews[probe]

    def createProbeView(self, probe):
        pview = WorkProbeView(self, probe)
        self.probeViews[probe] = pview
        self.mainGrid.addWidget(pview, self.tmpMainGridCount, 0)
        self.tmpMainGridCount += 1
        self.mainGrid.setRowStretch(self.tmpMainGridCount, 0)
        self.mainGrid.setRowStretch(self.tmpMainGridCount + 1, 1)
        self.mainGrid.update()

class WorkProbeView(AbstractChannelQFrame):
    def __init__(self, parent, probe):
        super(WorkProbeView, self).__init__(parent, probe)
        self.probeDict   = ChannelHandler.singleton.probes[probe]
        self.setBackgroundRole(QPalette.Window)
        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.targetName = self.probeDict['target']
        self.probeName  = probe

        loggers = self.probeDict['loggers']

        if 'btracker_logger_text' in loggers and \
           'btracker_logger_rrd' in loggers:
            viewType = 'text_and_rrdgraph'
        else: 
            viewType = 'text_only'

        # progress area
        progressFrame   = QFrame(self)
        progressGrid    = QGridLayout(self)
        self.timeoutProgress = TimeoutProgressBar(
            self, self.probeDict['timeout'] * 1000, 'Timeout: %p%')
        self.stepProgress    = StepProgressBar(
            self, self.probeDict['step'] * 1000, 'Step: %p%', self.timeoutProgress)
        progressGrid.addWidget(self.timeoutProgress,             0,0,1,1)
        progressGrid.addWidget(self.stepProgress,                1,0,2,1)
        progressGrid.setRowStretch(0,0)
        progressGrid.setRowStretch(1,1)
        progressGrid.setRowStretch(1,1)
        progressFrame.setLayout(progressGrid)

        self.leftFrame   = QFrame(self)
        self.probeInfo   = ProbeInfo(self,self.targetName,self.probeDict['id'],self.probeDict)
        self.textLog     = TextLog(self)
        self.rrdArea     = None

        leftGrid    = QGridLayout(self)
        if viewType == 'text_and_rrdgraph':
            self.setMinimumHeight(300)
            leftGrid.addWidget(self.probeInfo,       0,0,1,1)
            leftGrid.addWidget(progressFrame,   0,2,3,1)
            leftGrid.addWidget(self.textLog,         2,0,1,2)
            leftGrid.setContentsMargins(0,0,0,0)
            leftGrid.setVerticalSpacing(0)
            leftGrid.setHorizontalSpacing(0)
            leftGrid.setRowStretch(0,0)
            leftGrid.setRowStretch(1,1)
            leftGrid.setRowStretch(2,0)
            self.leftFrame.setLayout(leftGrid)
            self.rightPaneView   = QFrame(self)
            self.rrdArea    = RrdArea(self, self.probeDict)
            rightGrid = QGridLayout(self)
            rightGrid.setContentsMargins(0,0,0,0)
            rightGrid.addWidget(EventViewer(self),  0,0)
            rightGrid.addWidget(self.rrdArea,       1,0)
            self.rightPaneView.setLayout(rightGrid)

            grid = QGridLayout(self)
            grid.setContentsMargins(3,3,3,3)
            grid.setVerticalSpacing(0)
            grid.addWidget(self.leftFrame,       0,0,1,1)
            grid.addWidget(self.rightPaneView,   0,1,1,1)
            grid.setColumnStretch(0,0)
            grid.setColumnStretch(1,1)
            self.setLayout(grid)
        else:
            self.setMinimumHeight(200)
            leftGrid.addWidget(self.probeInfo,       0,0,1,1)
            leftGrid.addWidget(progressFrame,   0,2,3,1)
            leftGrid.setContentsMargins(0,0,0,0)
            leftGrid.setVerticalSpacing(0)
            leftGrid.setHorizontalSpacing(0)
            leftGrid.setRowStretch(0,0)
            leftGrid.setRowStretch(1,1)
            leftGrid.setRowStretch(2,0)
            self.leftFrame.setLayout(leftGrid)
            self.rightPaneView   = QFrame(self)
            rightGrid = QGridLayout(self)
            rightGrid.setContentsMargins(0,0,0,0)
            rightGrid.addWidget(EventViewer(self), 0,0)
            rightGrid.addWidget(self.textLog, 1,0)
            self.rightPaneView.setLayout(rightGrid)
            grid = QGridLayout(self)
            grid.setContentsMargins(3,3,3,3)
            grid.setVerticalSpacing(0)
            grid.addWidget(self.leftFrame,       0,0,1,1)
            grid.addWidget(self.rightPaneView,   0,1,1,1)
            grid.setColumnStretch(0,0)
            grid.setColumnStretch(1,1)
            self.setLayout(grid)


        self.connectProbe()
        #self.signal.connect(rightPaneView.handleEvent)
        #self.signal.connect(stepProgress.handleEvent)
        #self.signal.connect(textLog.handleEvent)
        #self.signal.connect(probeInfo.handleEvent)

    def handleProbeEvent(self, msg):
        msgType = msg['msgType']
        if msgType == 'probeDump':
            if msg['logger'] == 'btracker_logger_text':
                self.textLog.textDump(msg['data'])
            elif msg['logger'] == 'btracker_logger_rrd':
                self.rrdArea.rrdDump(msg['data'])
            elif msg['logger'] == 'tracker_events':
                print "logger tracker_events event"

        elif msgType == 'probeReturn':
            # log text
            self.textLog.textAppend(msg['value'])
            # progress
            self.stepProgress.resetProgress()
            # rrd
            if self.rrdArea != None: 
                self.rrdArea.updateGraph()

class EventViewer(QFrame):
    def __init__(self, parent):
        super(EventViewer, self).__init__(parent)
        toolTipBaseHexa = Monitor.MonitorMain.singleton.rgbDict['ToolTipBase']
        self.setStyleSheet("QFrame { border-radius: 15px; background: %s}" % toolTipBaseHexa)
        self.setFixedHeight(100)
        grid = QGridLayout(self)
        lab = QLabel('TODO frise chronologique des evenements et des status', self)
        grid.addWidget(lab, 0,0)
        self.setLayout(grid)

class TextLog(QTextEdit):
    def __init__(self, parent):
        super(TextLog, self).__init__(parent)
        dtext   = QTextDocument()
        dtext.setMaximumBlockCount(500)
        tformat = QTextCharFormat()
        tformat.setFontPointSize(8.2)
        self.setDocument(dtext)
        self.setCurrentCharFormat(tformat)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)

    def textDump(self, data):
        for line in data:
            self.append(str(line).rstrip())

    def textAppend(self, value):
        tstamp  = value['timestamp'] / 1000000
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        printable = string.replace('\n', ' ').replace('  ', ' ')
        self.append(time + "-> " + printable)

class ProbeInfo(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeInfo, self).__init__(parent)
        #self.setStyleSheet("QFrame { background: #00FF00 }")
        self.setFixedWidth(300)

        status      = probeDict['status']
        inspectors  = probeDict['inspectors']
        loggers     = probeDict['loggers']
        active      = probeDict['active']
        step        = probeDict['step']
        timeout     = probeDict['timeout']
        probeId     = probeDict['id']
        probeMod    = probeDict['probeMod']
        infoType    = probeDict['infoType']
        name        = probeDict['name']
        perm        = probeDict['perm']
        properties  = probeDict['properties']

        if (status == 'OK'):
            image = QSvgWidget(
                TkorderIcons.getImage('weather-clear'), self)
        elif (status == 'WARNING'):
            image = QSvgWidget(
                TkorderIcons.getImage('weather-showers'), self)
        elif (status == 'CRITICAL'):
            image = QSvgWidget(
                TkorderIcons.getImage('weather-severe-alert'), self)
        elif (status == 'UNKNOWN'):
            image = QSvgWidget(
                TkorderIcons.getImage('weather-few-clouds-night'), self)
        else:
            image = QSvgWidget(
                TkorderIcons.getImage('weather-clear-night'), self)
        statusLabel = QFrame(self)
        statusLabel.setFixedHeight(80)
        statusLabel.setFixedWidth(80)
        self.statusLabelContent = image
        statusGrid  = QGridLayout(self)
        statusGrid.addWidget(self.statusLabelContent,   0,0)
        statusLabel.setLayout(statusGrid)

        grid = QGridLayout(self)

        grid.addWidget(QLabel('Name:',  self),      1,0,1,1)
        grid.addWidget(QLabel(name,  self),         1,1,1,1)
        
        grid.addWidget(QLabel('Status:',    self),  2,0,1,1)
        grid.addWidget(QLabel(status, self),        2,1,1,1)

        grid.addWidget(QLabel('Active:', self),     3,0,1,1)
        grid.addWidget(QLabel(str(active),  self),  3,1,1,1)

        grid.addWidget(QLabel('Step:', self),       4,0,1,1)
        grid.addWidget(QLabel(str(step),  self),    4,1,1,1)

        grid.addWidget(QLabel('Timeout: ',  self),  5,0,1,1)
        grid.addWidget(QLabel(str(timeout),  self), 5,1,1,1)


        hLine = QFrame(self)
        hLine.setFrameShape(QFrame.HLine)
        hLine.setLineWidth(1)
        hLine.setMidLineWidth(1)
        hLine.setFrameShadow(QFrame.Sunken)
        grid.addWidget(hLine,                       6,0,1,3)

        #grid.addWidget(QLabel('Perm: ',  self),     7,0,1,1)
        #grid.addWidget(QLabel(str(perm),  self),    7,1,1,1)
        grid.addWidget(QPushButton('Force', self),     7,0,2,1)
        grid.addWidget(QPushButton('Suspend', self),   7,1,2,1)
        grid.addWidget(QPushButton('Gen Event', self),   7,2,2,1)

        grid.addWidget(statusLabel,            0,2,5,1)

        self.setLayout(grid)

class StepProgressBar(QProgressBar):
    
    " this progress bar control the TimeoutProbressBar start and stop "

    def __init__(self, parent, timerRange, textValue, timeoutProgress):
        super(StepProgressBar, self).__init__(parent)
        self.timeMax    = timerRange
        self.timeoutProgress    = timeoutProgress

        self.setOrientation(Qt.Vertical)
        self.setRange(0, timerRange)
        self.setFormat(textValue)
        self.setValue(40)
        self.setTextDirection(QProgressBar.TopToBottom)
        self.valueChanged.connect(self.handleValueChanged)

        self.timer = QTimeLine(timerRange, self)
        self.timer.setFrameRange(0, timerRange)
        self.timer.frameChanged[int].connect(self.setValue)

    def stopProgress(self):
        self.timer.stop()

    def startProgress(self):
        self.timer.start()

    def resetProgress(self):
        self.timeoutProgress.stopProgress()
        self.timeoutProgress.reset()
        self.stopProgress()
        self.startProgress()

    def handleValueChanged(self, i):
        if self.timeMax == i:
            self.timeoutProgress.startProgress()

class TimeoutProgressBar(QProgressBar):
    def __init__(self, parent, timerRange, textValue):
        super(TimeoutProgressBar, self).__init__(parent)
        self.timeMax = timerRange
        self.setOrientation(Qt.Vertical)
        self.setRange(0, timerRange)
        self.setFormat(textValue)
        self.setValue(40)
        self.setTextDirection(QProgressBar.TopToBottom)
        self.valueChanged.connect(self.handleValueChanged)

        self.timer = QTimeLine(timerRange, self)
        self.timer.setFrameRange(0, timerRange)
        self.timer.frameChanged[int].connect(self.setValue)

    def stopProgress(self):
        self.timer.stop()

    def startProgress(self):
        self.timer.start()

    def handleValueChanged(self, i):
        if self.timeMax == i: pass # do something
            

