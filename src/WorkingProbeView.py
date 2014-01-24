from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    WorkingProbeViewBody    import ProbeBody
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
from    LoggerViewText      import TextLog
from    LoggerViewRrds      import *
from    CustomButtons       import *
from    LoggerViewEventsTimeLine    import *
from    LoggerViewEventsTimeLineSimple    import *

import  TkorderIcons


class ProbeView(AbstractChannelQFrame):
    def __init__(self, parent, probe):
        super(ProbeView, self).__init__(parent, probe)
        self.probeDict   = ChannelHandler.singleton.probes[probe]
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Sunken)
        self.targetName = self.probeDict['target']
        self.probeName  = probe
        self.parent = parent

        loggers = self.probeDict['loggers']

        if 'btracker_logger_text' in loggers and \
           'btracker_logger_rrd' in loggers:
            viewType = 'text_and_rrdgraph'
        else: 
            viewType = 'text_only'


        # head
        self.head = ProbeHead(self, probe)

        # body 
        self.body       = ProbeBody(self, viewType, self.probeDict)
        self.bodyInit   = False

        # tabulation
        tab = QFrame(self)
        tab.setFixedWidth(20)

        self.grid = QGridLayout(self)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.grid.addWidget(self.head,  0, 0, 1, 2)
        self.grid.addWidget(tab,        1, 0)
        self.grid.addWidget(self.body,  1, 1)
        

        self.setLayout(self.grid)
        self.toggleBody()
        self.connectProbe()

    def toggleBody(self):
        if self.grid.itemAtPosition(1,1) == None:
            if self.bodyInit == False: self.body.show()
            self.grid.addWidget(self.body, 1, 1)
        else:
            self.body.hide()
            self.grid.removeWidget(self.body)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeReturn':
            self.parent.updateToolTip(msg)

        self.head.handleProbeEvent(msg)
        self.body.handleProbeEvent(msg)

#############################
# HEAD
#############################
class ProbeHead(QFrame):
    def __init__(self, parent, probe):
        super(ProbeHead, self).__init__(parent)
        
        self.label   = HeadProbeLabel(self, probe)
        self.timeLine   = SimpleTimeLine(self)
        #self.control = HeadProbeControl(self, probe, parent)
        #self.options = HeadProbeOptions(self, probe)
        self.progress = HeadProbeProgress(self, probe)
        self.showHistory = QCheckBox('Show history', self)
        self.showHistory.clicked.connect(parent.toggleBody)

        self.setFixedHeight(120)
        grid = QGridLayout(self)
        grid.addWidget(self.label,          0,0)
        grid.addWidget(self.progress,       0,1)
        #grid.addWidget(self.options,        0,2)
        grid.addWidget(self.timeLine,       1,1)
        grid.addWidget(self.showHistory,    2,0)
        #grid.addWidget(self.control, 1,0,1,1)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,0)
        self.setLayout(grid)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeReturn':
            self.handleReturn(msg)

        self.timeLine.handleProbeEvent(msg)

    def handleReturn(self, msg):
        #self.body.handleReturn(msg)
        self.progress.handleReturn(msg)

class HeadProbeLabel(QFrame):
    def __init__(self, parent, probe):
        super(HeadProbeLabel, self).__init__(parent)
        self.probeDict  = ChannelHandler.singleton.probes[probe]
        self.target     = self.probeDict['target']
        self.probe      = self.probeDict['name']
        self.setFixedWidth(200)
        self.setContentsMargins(0,0,0,0)

        self.probeLabel = self._setLabel(self.probeDict['status'])
        sigDict = ChannelHandler.singleton.masterSignalsDict
        sigDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.probeLabel, 0,0)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.grid.setRowStretch(0,0)
        self.grid.setRowStretch(1,1)
        self.grid.setVerticalSpacing(0)
        self.grid.setHorizontalSpacing(0)
        self.setLayout(self.grid)

    def _setLabel(self, status):
        if   status == 'OK':
            return ProbeOkButton(self, self.probe)
        elif status == 'WARNING':
            return ProbeWarningButton(self, self.probe)
        elif status == 'UNKNOWN':
            return ProbeUnknownButton(self, self.probe)
        elif status == 'CRITICAL':
            return ProbeCriticalButton(self, self.probe)

    def _updateLabel(self, status):
        self.grid.removeWidget(self.probeLabel)
        self.probeLabel.hide()
        self.probeLabel.deleteLater()
        self.probeLabel = self._setLabel(status)
        self.grid.addWidget(self.probeLabel, 0,0)

    def _handleProbeInfo(self, msg):
        target = msg['value']['target']
        probe  = msg['value']['name']
        if target == self.target:
            if probe == self.probe:
                status = msg['value']['status']
                self._updateLabel(status)

class HeadProbeProgress(QFrame):
    def __init__(self, parent, probe):
        super(HeadProbeProgress, self).__init__(parent)
        self.probeDict   = ChannelHandler.singleton.probes[probe]
        grid = QGridLayout(self)

        # progress timeout and step
        self.timeoutProgress = TimeoutProgressBar(
            self, self.probeDict['timeout'] * 1000, 'Timeout: %p%')
        self.stepProgress    = StepProgressBar(
            self, self.probeDict['step'] * 1000, 'Step: %p%', self.timeoutProgress)
        checkProgressLabel  = QLabel('Step progress: ', self)
        grid.addWidget(checkProgressLabel,      0,2)
        grid.addWidget(self.stepProgress,       0,3)
        stepLabel           = QLabel('Step: ', self)
        grid.addWidget(stepLabel,                   0,0)
        grid.addWidget(BoldLabel('%i seconds' % self.probeDict['step'], self), 0,1)

        timeoutLabel        = QLabel('Timeout: ', self)
        grid.addWidget(timeoutLabel,                1,0)
        grid.addWidget(BoldLabel('%i seconds' % self.probeDict['timeout'], self), 1,1)
        timeoutProgressLabel = QLabel('Timeout progress: ', self)
        grid.addWidget(timeoutProgressLabel,    1,2)
        grid.addWidget(self.timeoutProgress,    1,3)

        lastReturnTimeLabel = QLabel('Last return: ', self)
        self.lastReturnTime = BoldLabel('', self)
        grid.addWidget(lastReturnTimeLabel,         2,0)
        grid.addWidget(self.lastReturnTime,         2,1)

        lastReturnValueLabel = QLabel('Last return value: ', self)
        grid.addWidget(lastReturnValueLabel,        2,2)

        self.lastReturnValue = QTextEdit(self)
        self.lastReturnValue.setTextInteractionFlags(Qt.NoTextInteraction)
        self.lastReturnValue.setFixedHeight(20)
        self.lastReturnValue.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lastReturnValue.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lastReturnValue.setLineWrapMode(QTextEdit.NoWrap)

        grid.addWidget(self.lastReturnValue,        2,3)

    def _setLastReturn(self, msg):
        ts      = msg['value']['timestamp'] / 1000000
        time    = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        rep     = msg['value']['originalRep'].rstrip()
        printable = rep.replace('\n', ' ').replace('  ', ' ')
        self.lastReturnTime.setText(time)
        self.lastReturnValue.setText(printable)

    def handleReturn(self, msg):
        self._setLastReturn(msg)
        self.lastReturnValue.setToolTip(msg['value']['originalRep'])
        self.stepProgress.resetProgress()

class HeadProbeControl(QFrame):
    def __init__(self, parent, probe, toggler):
        super(HeadProbeControl, self).__init__(parent)

        self.action = QPushButton('Actions', self)

        self.toggle = QPushButton('Details', self)
        self.toggle.clicked.connect(toggler.toggleBody)

        grid = QGridLayout(self)
        grid.addWidget(self.action,     1,0)
        grid.addWidget(self.toggle,     2,0)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,0)
        self.setLayout(grid)


class ProbeConfig(QFrame):
    def __init__(self, parent, probe):
        super(ProbeConfig, self).__init__(parent)
        self.probeDict   = ChannelHandler.singleton.probes[probe]


        grid = QGridLayout(self)

        moduleLabel         = QLabel('Check module: ', self)
        grid.addWidget(moduleLabel,                 2,0)
        grid.addWidget(BoldLabel(self.probeDict['probeMod'], self), 2,1)

        if self.probeDict['probeMod'] == 'btracker_probe_nagios':
            checkCommand        = QLabel('Command: ', self)
            grid.addWidget(checkCommand,                 2,2)
            grid.addWidget(BoldLabel(self.probeDict['probeconf'], self), 2,3)

        targetName          = QLabel('Target name: ', self)
        grid.addWidget(targetName,                  4,0)
        grid.addWidget(BoldLabel(self.probeDict['target'], self), 4,1)

        targetIpLabel       = QLabel('Target IP address: ', self)
        targetIp = ChannelHandler.singleton.targets[self.probeDict['target']]

        grid.addWidget(targetIpLabel,               4,2)
        grid.addWidget(BoldLabel('192.168.0.1', self), 4,3)


        inspectStr = ''
        for inspector in self.probeDict['inspectors'].keys():
            inspectStr += '%s |  ' % inspector.title()

        inspectorsLabel     = QLabel('Inspectors: ', self)
        grid.addWidget(inspectorsLabel,             8,0)
        grid.addWidget(BoldLabel(inspectStr, self), 8,1,1,4)

        logStr     = ''
        for logger in self.probeDict['loggers'].keys():
            logStr += '%s | ' % logger.title()

        loggersLabel        = QLabel('Loggers: ', self)
        grid.addWidget(loggersLabel,                10,0)
        grid.addWidget(BoldLabel(logStr, self),     10,1,1,4)

        lastReturnTimeLabel = QLabel('Last return: ', self)
        self.lastReturnTime = BoldLabel('', self)
        grid.addWidget(lastReturnTimeLabel,         12,0)
        grid.addWidget(self.lastReturnTime,         12,1)

        lastReturnValueLabel = QLabel('Last return value: ', self)
        self.lastReturnValue = BoldLabel('', self)
        self.lastReturnValue.setMaximumWidth(500)
        grid.addWidget(lastReturnValueLabel,        12,2)
        grid.addWidget(self.lastReturnValue,        12,3,1,2)

        self.statusHistory   = SimpleTimeLine(self)
        statusHistoryLabel  = QLabel('Status History: ', self)
        grid.addWidget(statusHistoryLabel,      14,0)
        grid.addWidget(self.statusHistory,      14,1)

        self.setLayout(grid)


    def handleReturn(self, msg):
        self._setLastReturn(msg)

    def _setLastReturn(self, msg):
        ts      = msg['value']['timestamp'] / 1000000
        time    = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        rep     = msg['value']['originalRep'].rstrip()
        printable = rep.replace('\n', ' ').replace('  ', ' ')
        self.lastReturnTime.setText(time)
        self.lastReturnValue.setText(printable)


class BoldLabel(QLabel):
    def __init__(self, text, parent):
        super(BoldLabel, self).__init__(parent)
        self.setTextFormat(Qt.RichText)
        self.setText(text)

    def setText(self, text):
        QLabel.setText(self,'<span style="font-weight:600;"> %s </span>' % text)

class HeadProbeOptions(QFrame):
    def __init__(self, parent, probe):
        super(HeadProbeOptions, self).__init__(parent)
        self.promoteCheck = QCheckBox('include in Dashboard', self)
        grid = QGridLayout(self)
        grid.addWidget(self.promoteCheck, 0,0)
        self.setLayout(grid)

#############################
# BODY
#############################
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
        self.setInvertedAppearance(True)
        self.timeMax    = timerRange
        self.setTextVisible(False)
        self.timeoutProgress    = timeoutProgress
        self.setStyleSheet('QProgressBar {  \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #555753,    \
                stop: 1 #888a85);           \
            height: 2px;            \
            text-align: center;            \
            border: 2px solid;      \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            max-height: 5px;            \
            min-height: 5px;            \
            border-color: #888a85;      \
        } \
        QProgressBar::chunk {      \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #a1d99b,    \
                stop: 1 #74c476);           \
            width: 10px;           \
            margin: 0.5px;           \
        }')

        self.setOrientation(Qt.Horizontal)
        self.setRange(0, timerRange)
        self.setFormat(textValue)
        self.setValue(40)
        self.setTextDirection(QProgressBar.TopToBottom)
        self.valueChanged.connect(self.handleValueChanged)

        # TODO move QTimeLine in a thread
        self.timer = QTimeLine(timerRange, self)
        self.timer.setUpdateInterval(80)
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
        self.setTextVisible(False)
        self.setOrientation(Qt.Horizontal)
        self.setRange(0, timerRange)
        self.setFormat(textValue)
        self.setValue(40)
        self.setTextDirection(QProgressBar.TopToBottom)
        self.valueChanged.connect(self.handleValueChanged)
        self.setStyleSheet('QProgressBar {  \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #555753,    \
                stop: 1 #888a85);           \
            height: 2px;            \
            text-align: center;            \
            border: 2px solid;      \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            max-height: 5px;            \
            min-height: 5px;            \
            border-color: #888a85;      \
        } \
        QProgressBar::chunk {      \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #ef2929,    \
                stop: 1 #cc0000);           \
            width: 10px;           \
            margin: 0.5px;           \
        }')

        # TODO move QTimeLine in a thread
        self.timer = QTimeLine(timerRange, self)
        self.timer.setUpdateInterval(80)
        self.timer.setFrameRange(0, timerRange)
        self.timer.frameChanged[int].connect(self.setValue)

    def stopProgress(self):
        self.timer.stop()

    def startProgress(self):
        self.timer.start()

    def handleValueChanged(self, i):
        if self.timeMax == i: pass # do something
