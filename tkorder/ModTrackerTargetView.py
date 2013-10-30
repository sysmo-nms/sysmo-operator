from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  datetime
import  TkorderIcons
import  ModTracker

class Stack(QStackedWidget):
    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.stackDict       = dict()

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
        " these messages unstack target specified in the msg"
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

class ElementView(QFrame):
    def __init__(self, parent, targetName):
        super(ElementView, self).__init__(parent)
        self.head = ElementViewHead(self, targetName)
        self.body = ElementViewBody(self, targetName)
        grid = QGridLayout()
        grid.addWidget(self.head, 0, 0)
        grid.addWidget(self.body, 1, 0)
        self.setLayout(grid)

    def handleProbeReturn(self, msg):
        self.body.handleProbeReturn(msg)
        
class ElementViewHead(QFrame):
    def __init__(self, parent, targetName):
        super(ElementViewHead, self).__init__(parent)
        self.headLabel = QLabel(targetName)
        self.headLabel.setFrameStyle(1),
        self.headLabel.setFrameShadow(QFrame.Raised)
        grid = QGridLayout()
        grid.addWidget(self.headLabel, 0, 0)
        self.setLayout(grid)

class ElementViewBody(QScrollArea):
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


class ProbeView(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeView, self).__init__(parent)
        self.setFrameStyle(1)
        self.setFrameShadow(QFrame.Sunken)

        self.label      = QLabel("probe id: "+ `probeId`, self)
        self.logArea    = QTextEdit(self)
        self.logArea.setReadOnly(True)
        self.logArea.setLineWrapMode(QTextEdit.NoWrap)
        grid = QGridLayout()
        grid.addWidget(self.label,   0,0)
        grid.addWidget(self.logArea, 1,0)
        self.setLayout(grid)

    def handleProbeReturn(self,msg):
        value   = msg['value']
        tstamp  = value['timestamp']
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        self.logArea.append(time + "-> " + string)
