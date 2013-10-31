from    PySide      import QtGui, QtCore
import  TkorderIcons
import  Supercast
import  ModTrackerTree
import  ModTrackerCube
import  ModTrackerTargetView

class TrackerMain(QtGui.QSplitter):
    @classmethod
    def initView(cls):
        stack = cls.singleton.rightStack
        stack.addWidget(ModTrackerCube.View(cls.singleton))

    @classmethod
    def setView(cls, item):
        if   item.data(QtCore.Qt.UserRole) == 'target':
            target  = item
            probeId = None 
        elif item.data(QtCore.Qt.UserRole) == 'probe':
            target = ModTrackerTree.TrackerTViewModel.findTargetByName(
                item.data(QtCore.Qt.UserRole + 2))
            probeId = item.data(QtCore.Qt.UserRole + 1)

        targetName      = target.data(QtCore.Qt.UserRole + 1)
        Supercast.Link.subscribe(targetName)
        rightStack = cls.singleton.rightStack
        rightStack.setView(target, probeId)

    def __init__(self, parent):
        super(TrackerMain, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        Supercast.Link.setMessageProcessor('modTrackerPDU', self.handleMsg)

        " splitter test "
        self.splitterMoved.connect(self.splitterMoving)

        self.leftTree   = ModTrackerTree.TreeContainer(self)
        self.rightStack = ModTrackerTargetView.Stack(self)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightStack)
        
        self.targets    = dict()
        TrackerMain.singleton = self
        TrackerMain.initView()

    def handleProbeInfo(self, msg):
        # TODO integrade the targets dict() with ModTrackerTree
        probeInfo   = msg['value']
        channel     = probeInfo['channel']
        probeId     = probeInfo['id']
        if channel in self.targets:
            self.targets[channel][probeId]  = probeInfo
        else:
            self.targets[channel]           = dict()
            self.targets[channel][probeId]  = probeInfo

        ModTrackerTree.handle(msg)

    def handleMsg(self, msg):
        mType = msg['msgType']

        if   (mType == 'probeInfo'):
            #print "received probeInfo"
            self.handleProbeInfo(msg)
        elif (mType == 'targetInfo'):
            #print "received targetInfo"
            ModTrackerTree.handle(msg)
        elif (mType == 'probeModInfo'):
            #print "received probeModInfo"
            ModTrackerTree.handle(msg)
        elif (mType == 'probeActivity'): pass
            #print "received probeActivity"
        elif (mType == 'subscribeOk'): pass
        elif (mType == 'probeDump'):
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

class Stack(QtGui.QStackedWidget):
    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.stackDict       = dict()

    def setView(self, targetItem, probeId):
        targetName      = targetItem.data(QtCore.Qt.UserRole + 1)
        # target is allready set?
        if targetName in self.stackDict.keys():
            self.setCurrentWidget(self.stackDict[targetName])
            return

        # temp XXX
        targetDict = self._itemToDict(targetItem)
        # then create the widget
        stackWidget = ModTrackerGraphite.ElementView(
            self, targetName, probeId, targetDict)
        self.addWidget(stackWidget)
        self.stackDict[targetName] = stackWidget

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

    def _itemToDict(self, item):
        print item.data(QtCore.Qt.UserRole + 2), "lkj"

