from    PySide      import QtGui, QtCore
from    TkorderMain import *
from    Viewers     import Wide, Target
from    TreeArea    import Tree
import  TkorderIcons
import  Supercast

class TrackerWindow(QtGui.QSplitter):
    @classmethod
    def setMyself(cls, myself):
        cls._myself = myself

    @classmethod
    def myself(cls):
        return cls._myself

    @classmethod
    def initView(cls):
        stack = cls._myself.rightStack
        stack.addWidget(Wide.View(cls._myself))

    @classmethod
    def setView(cls, item):
        if   item.data(QtCore.Qt.UserRole) == 'target':
            target  = item
            probeId = None 
        elif item.data(QtCore.Qt.UserRole) == 'probe':
            target = Tree.TrackerTViewModel.findTargetByName(
                item.data(QtCore.Qt.UserRole + 2))
            probeId = item.data(QtCore.Qt.UserRole + 1)

        targetName      = target.data(QtCore.Qt.UserRole + 1)
        Supercast.Link.subscribe(targetName)
        rightStack = cls._myself.rightStack
        rightStack.setView(target, probeId)

    @classmethod
    def setMaxOpenStacks(cls, num):
        cls.maxOpenStacks = num

    def __init__(self, parent):
        super(TrackerWindow, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        Supercast.Link.setMessageProcessor('modTrackerPDU', self.handleMsg)

        " splitter test "
        self.splitterMoved.connect(self.splitterMoving)

        self.leftTree   = Tree.TreeContainer(self)
        self.rightStack = Stack(self)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightStack)
        
        TrackerWindow.setMyself(self)
        TrackerWindow.initView()

    def handleMsg(self, msg):
        mType = msg['msgType']

        if   (mType == 'probeInfo'):
            #print "received probeInfo"
            Tree.handle(msg)
        elif (mType == 'targetInfo'):
            #print "received targetInfo"
            Tree.handle(msg)
        elif (mType == 'probeModInfo'):
            #print "received probeModInfo"
            Tree.handle(msg)
        elif (mType == 'probeActivity'): pass
            #print "received probeActivity"
        elif (mType == 'subscribeOk'): pass
        elif (mType == 'unsubscribeOk'):
            self.rightStack.unsubscribeOkMsg(msg)
        else:
            print "unknown message type: ", mType
    
    def splitterMoving(self, a, b): pass

    def updateEvent(self, event):
        TrackerWindow.setView(event)

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

        # then create the widget
        stackWidget = Target.ElementView(self, targetName, probeId)
        self.addWidget(stackWidget)
        self.stackDict[targetName] = stackWidget

        # set it current:
        self.setCurrentWidget(stackWidget)
        return

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
