from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    TargetRrdView   import RrdView
import  os
import  datetime
import  TkorderIcons
import  ModTracker

class ProbeView(QFrame):

    signal = Signal(dict)

    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeView, self).__init__(parent)
        self.vardir     = ModTracker.TrackerMain.singleton.vardir
        self.probeConf  = probeDict
        loggers = probeDict['loggers']

        if 'btracker_logger_text' in loggers and \
           'btracker_logger_rrd' in loggers:
            viewType = 'full'
        else: viewType = 'text'

        self.setFrameShape(QFrame.StyledPanel)
        #self.setStyleSheet("QFrame { background: #0000FF }")
        self.setFixedHeight(300)
        grid = QGridLayout()
        grid.setContentsMargins(3,3,3,3)
        grid.addWidget(ProbeInfo(self,targetName,probeId,probeDict),    0,0)
        grid.addWidget(TextLog(self),                                   1,0)
        grid.addWidget(RrdView(self, probeDict),    0,1,2,1)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
    
        self.setLayout(grid)


    def setSignal(self, signalObj):
        signalObj.signal.connect(self.handleEvent)

    def handleEvent(self, msg):
        self.signal.emit(msg)

    def btrackerLoggerRrdDump(self, msg):
        chan    = msg['value']['channel']
        pid     = msg['value']['id']
        data    = msg['value']['data']

        rrdFile = os.path.join(self.vardir, chan + '-' + str(pid) + '.rrd')
        f       = open(rrdFile, 'wb')
        f.write(data)
        f.close()
        self.rrdFile = rrdFile
        self.graphRrds()

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
        self.setFixedWidth(300)
        self.setFixedHeight(90)
        parent.signal.connect(self.handleEvent)

    def handleEvent(self, msg):
        print msg['msgType']
        if   msg['msgType'] == 'probeDump':
            if msg['value']['logger'] == 'btracker_logger_text':
                self.textDump(msg['value']['data'])
            return
        elif msg['msgType'] == 'probeReturn':
            self.textAppend(msg['value'])

    def textDump(self, data):
        self.append(str(data).rstrip())

    def textAppend(self, value):
        tstamp  = value['timestamp']
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        printable = string.replace('\n', ' ').replace('  ', ' ')
        self.append(time + "-> " + printable)

 
class ProbeInfo(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeInfo, self).__init__(parent)
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

        grid = QGridLayout()

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
        grid.addWidget(hLine,                       6,0,1,2)

        grid.addWidget(QLabel('Perm: ',  self),     7,0,1,1)
        grid.addWidget(QLabel(str(perm),  self),    7,1,1,1)

        # progress bars
        timeoutProgress = TimeoutProgressBar(
            self, timeout * 1000, 'Timeout: %p%')
        stepProgress    = StepProgressBar(
            self, step * 1000, 'Step: %p%', timeoutProgress)

        grid.addWidget(stepProgress,                1,2,7,1)
        grid.addWidget(timeoutProgress,             1,3,7,1)
        
        parent.signal.connect(stepProgress.handleEvent)

        #self.stepCounter    = stepProgress
        #self.timeoutCounter = timeoutProgress
        #self.step       = step
        #self.timeout    = timeout
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

    def handleEvent(self, msg):
        if msg['msgType'] == 'probeReturn': self.resetProgress()

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
        if self.timeMax == i:
            print "timeout reached", str(i)

