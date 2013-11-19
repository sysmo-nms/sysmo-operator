from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Supercast
import  ModTrackerTreeArea
import  ModTrackerWideView
import  ModTrackerTargetView

class TrackerMain(QSplitter):
    " Them main window. Emit tracker server events, and forward childs "
    " events to other childs."

    @classmethod
    def initView(cls):
        stack = cls.singleton.rightStack
        stack.addWidget(ModTrackerWideView.View(cls.singleton))

    @classmethod
    def setView(cls, item):
        if   item.data(Qt.UserRole) == 'target':
            target  = item
            probeId = None 
        elif item.data(Qt.UserRole) == 'probe':
            target = ModTrackerTreeArea.TrackerTViewModel.findTargetByName(
                item.data(Qt.UserRole + 2))
            probeId = item.data(Qt.UserRole + 1)

        targetName      = target.data(Qt.UserRole + 1)
        Supercast.Link.subscribe(targetName)
        rightStack = cls.singleton.rightStack
        rightStack.setView(target, probeId)

    def __init__(self, parent):
        super(TrackerMain, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        Supercast.Link.setMessageProcessor('modTrackerPDU', self.handleMsg)

        " splitter test "
        self.splitterMoved.connect(self.splitterMoving)

        self.leftTree   = ModTrackerTreeArea.TreeContainer(self)
        self.rightStack = ModTrackerTargetView.Stack(self)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightStack)
        
        self.targets    = dict()
        TrackerMain.singleton = self
        TrackerMain.initView()

    def handleProbeInfo(self, msg):
        # TODO integrade the targets dict() with ModTrackerTreeArea
        probeInfo   = msg['value']
        channel     = probeInfo['channel']
        probeId     = probeInfo['id']
        if channel in self.targets:
            self.targets[channel][probeId]  = probeInfo
        else:
            self.targets[channel]           = dict()
            self.targets[channel][probeId]  = probeInfo

        ModTrackerTreeArea.handle(msg)

    def handleMsg(self, msg):
        mType = msg['msgType']

        if   (mType == 'probeInfo'):
            #print "received probeInfo"
            self.handleProbeInfo(msg)
        elif (mType == 'targetInfo'):
            #print "received targetInfo"
            ModTrackerTreeArea.handle(msg)
        elif (mType == 'probeModInfo'):
            #print "received probeModInfo"
            ModTrackerTreeArea.handle(msg)
        elif (mType == 'probeActivity'):
            pass
            #print "received probeActivity"
        elif (mType == 'subscribeOk'):
            pass
        elif (mType == 'probeDump'):
            self.probeDumpSignal.emit()
            #print "dump from ", msg['value']['logger']
            self.rightStack.handleProbeDump(msg)
        elif (mType == 'probeReturn'):
            self.rightStack.handleProbeReturn(msg)
        elif (mType == 'unsubscribeOk'):
            self.rightStack.unsubscribeOkMsg(msg)
        else:
            print "unknown message type: ", mType
    
    def splitterMoving(self, a, b): pass

    def updateEvent(self, event):
        TrackerMain.setView(event)

    def getTargetInfo(self, target):
        print "will return target dict", target
