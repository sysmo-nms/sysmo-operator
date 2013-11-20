from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile

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
        grid.addWidget(QLabel("hell", self),    0,1,1,2)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
    
        self.setLayout(grid)

    def setSignal(self, signalObj):
        signalObj.signal.connect(self.handleEvent)

    def handleEvent(self, msg):
        print "event!"
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
        grid.addWidget(QLabel('status: ' + status,  self),  0,0,1,1)
        grid.addWidget(QLabel('active: ' + str(active),  self),  1,0,1,1)
        grid.addWidget(QLabel('step: ' + str(step),  self),      2,0,1,1)
        grid.addWidget(QLabel('timeout: ' + str(timeout),  self), 3,0,1,1)
        grid.addWidget(QLabel('name: ' + name,  self),      4,0,1,1)
        grid.addWidget(QLabel('perm: ' + str(perm),  self),      5,0,1,1)
        grid.setRowStretch(50, 1)
        self.setLayout(grid)
