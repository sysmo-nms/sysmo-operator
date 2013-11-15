from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool

class Stack(QStackedWidget):
    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.stackDict       = dict()
        Stack.vardir = os.path.join(os.getcwd(), 'var')

    def setView(self, targetItem, probeId):
        targetName      = targetItem.data(Qt.UserRole + 1)
        # target is allready set?
        if targetName in self.stackDict.keys():
            self.setCurrentWidget(self.stackDict[targetName])
            return

        # and create the widget
        stackWidget = ElementView(self, targetName)
        self.addWidget(stackWidget)
        self.stackDict[str(targetName)] = stackWidget

        # set it current:
        self.setCurrentWidget(stackWidget)
        return

    def dumpMsg(self, msg):
        print "dump"

    def returnMsg(self, msg):
        print "return"

    def unsubscribeOkMsg(self, msg):
        " these messages unstack the target specified in the msg"
        key = msg['value']
        if key in self.stackDict.keys():
            stackWidget = self.stackDict[key]
            # remove from stack
            self.removeWidget(stackWidget)
            # destroy it
            stackWidget.destroy()
            # then remove it from stackDict
            del self.stackDict[key]
        return

    def handleProbeReturn(self, msg):
        chan = msg['value']['channel'] 
        if chan in self.stackDict:
            self.stackDict[chan].handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        chan = msg['value']['channel']
        if chan in self.stackDict:
            self.stackDict[chan].handleProbeDump(msg)

class ElementView(QFrame):
    def __init__(self, parent, targetName):
        super(ElementView, self).__init__(parent)
        self.head = ElementViewHead(self, targetName)
        self.scroll = ElementViewScroll(self, targetName)
        grid = QGridLayout()
        grid.addWidget(self.head, 0, 0)
        grid.addWidget(self.scroll, 1, 0)
        self.setLayout(grid)

    def handleProbeReturn(self, msg):
        self.scroll.handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        self.scroll.handleProbeDump(msg)
        
class ElementViewHead(QFrame):
    def __init__(self, parent, targetName):
        super(ElementViewHead, self).__init__(parent)
        self.headLabel = QLabel(targetName)
        self.headLabel.setFrameStyle(1),
        self.headLabel.setFrameShadow(QFrame.Raised)
        grid = QGridLayout()
        grid.addWidget(self.headLabel, 0, 0)
        self.setLayout(grid)

class ElementViewScroll(QScrollArea):
    def __init__(self, parent, targetName):
        super(ElementViewScroll, self).__init__(parent)
        self.content = ElementViewBody(self, targetName)
        self.setWidget(self.content)
        self.setWidgetResizable(True)

    def handleProbeReturn(self, msg):
        self.content.handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        self.content.handleProbeDump(msg)

class ElementViewBody(QFrame):
    def __init__(self, parent, targetName):
        super(ElementViewBody, self).__init__(parent)
        targetDict = ModTracker.TrackerMain.singleton.targets[targetName]
        self.grid = QGridLayout()
        for probeId in targetDict:
            self.grid.addWidget(ProbeView(self, 
                targetName, probeId, targetDict[probeId]), probeId, 0)
        self.setLayout(self.grid)

    def handleProbeReturn(self, msg):
        probeId     = msg['value']['id']
        probeLayout = self.grid.itemAtPosition(probeId, 0)
        probeView   = probeLayout.widget()
        probeView.handleProbeReturn(msg)

    def handleProbeDump(self, msg):
        probeId     = msg['value']['id']
        probeLayout = self.grid.itemAtPosition(probeId, 0)
        probeView   = probeLayout.widget()
        probeView.handleProbeDump(msg)


class ProbeView(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeView, self).__init__(parent)
        self.setFrameStyle(1)
        self.setFixedHeight(350)
        self.setFrameShadow(QFrame.Sunken)

        self.infoLabel  = ProbeInfos(self, targetName, probeId, probeDict)
        self.rrdButtons = ProbeButtons(self, probeDict)
        self.rrdGraphs  = ProbeGraphs(self, probeDict)

        self.logArea    = QTextEdit(self)
        dtext   = QTextDocument()
        dtext.setMaximumBlockCount(500)
        tformat = QTextCharFormat()
        tformat.setFontPointSize(8.2)
        self.logArea.setDocument(dtext)
        self.logArea.setCurrentCharFormat(tformat)
        self.logArea.setReadOnly(True)
        self.logArea.setLineWrapMode(QTextEdit.NoWrap)
        self.logArea.setFixedHeight(90)



        grid = QGridLayout()
        grid.addWidget(self.infoLabel,   0,0,1,1)
        grid.addWidget(self.rrdButtons,  0,1,1,1)
        grid.addWidget(self.rrdGraphs,   0,2,1,1)
        grid.addWidget(self.logArea,     1,0,1,3)

        grid.setRowStretch(0,1)
        grid.setRowStretch(1,0)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)

        self.setLayout(grid)

    def handleProbeReturn(self,msg):
        value   = msg['value']
        tstamp  = value['timestamp']
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        printable = string.replace('\n', ' ').replace('  ', ' ')

        doc = self.logArea.document()
        print "line count is ", doc.blockCount()
        self.logArea.append(time + "-> " + printable)
        #self.logArea.append(str(tstamp) + ">>>" + string)

    def handleProbeDump(self, msg):
        # TODO format each timestamp to match the handleProbeReturn print
        if msg['value']['logger'] == 'btracker_logger_text':
            self.btrackerLoggerTextDump(msg)
        else:
            self.btrackerLoggerRrdDump(msg)

    def btrackerLoggerTextDump(self, msg):
        self.logArea.append(str(msg['value']['data']).rstrip())

    def btrackerLoggerRrdDump(self, msg):
        chan    = msg['value']['channel']
        pid     = msg['value']['id']
        data    = msg['value']['data']
        vardir  = Stack.vardir
        rrdFile = os.path.join(vardir, chan + '-' + str(pid) + '.rrd')
        f       = open(rrdFile, 'wb')
        f.write(data)
        f.close()

class ProbeInfos(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeInfos, self).__init__(parent)
        grid = QGridLayout()
        grid.addWidget(QLabel(targetName + '-' + str(probeId), self), 0,0,1,1)
        self.setLayout(grid)

class ProbeButtons(QFrame):
    def __init__(self, parent, probeDict):
        super(ProbeButtons, self).__init__(parent)
        grid = QGridLayout()
        grid.addWidget(QLabel('buttons!', self), 0,0,1,1)
        self.setLayout(grid)

class ProbeGraphs(QFrame):
    def __init__(self, parent, probeDict):
        super(ProbeGraphs, self).__init__(parent)
        grid = QGridLayout()
        grid.addWidget(QLabel('graphs!', self), 0,0,1,1)
        self.setLayout(grid)
