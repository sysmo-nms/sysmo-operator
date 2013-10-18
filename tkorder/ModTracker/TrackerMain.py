from    PySide import QtGui, QtCore
import  TkorderIcons
import  TkorderMain
import  PowerTree
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
        stack.addWidget(WideView(cls._myself))

    @classmethod
    def setView(cls, item):
        if   item.data(QtCore.Qt.UserRole) == 'target':
            target  = item
            probeId = None 
        elif item.data(QtCore.Qt.UserRole) == 'probe':
            target = PowerTree.TrackerTViewModel.findTargetByName(
                item.data(QtCore.Qt.UserRole + 2))
            probeId = item.data(QtCore.Qt.UserRole + 1)

        targetName      = target.data(QtCore.Qt.UserRole + 1)
        print "i should subscribe to: ", targetName
        Supercast.Socket.subscribe(targetName)
        rightStack = cls._myself.rightStack
        rightStack.setView(target, probeId)

    @classmethod
    def setMaxOpenStacks(cls, num):
        cls.maxOpenStacks = num

    def __init__(self, parent):
        super(TrackerWindow, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        Supercast.Socket.my.setMessageProcessor('modTrackerPDU', self.handleMsg)

        self.leftTree   = PowerTree.PowerTreeContainer(self)
        self.rightStack = RightPane(self)
        self.rightStack.setMaxOpenChans(3)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightStack)
        
        TrackerWindow.setMyself(self)
        TrackerWindow.initView()

    def handleMsg(self, msg):
        mType = msg['msgType']

        if   (mType == 'probeInfo'):
            print "received probeInfo"
            PowerTree.handle(msg)
        elif (mType == 'targetInfo'):
            print "received targetInfo"
            PowerTree.handle(msg)
        elif (mType == 'probeModInfo'):
            print "received probeModInfo"
            PowerTree.handle(msg)
        elif (mType == 'probeActivity'):
            print "received probeActivity", msg
        else:
            print "unknown message type: ", mType



class RightPane(QtGui.QStackedWidget):
    def __init__(self, parent):
        super(RightPane, self).__init__(parent)
        self.maxOpenChans   = 3
        self.chanList       = None

    def setView(self, target, probeId):
        targetName      = target.data(QtCore.Qt.UserRole + 1)
        currentWidget   = self.widget(1)
        if currentWidget == None:
            self.insertWidget(1, ElementView(self, targetName, probeId))
        else:
            self.removeWidget(currentWidget)
            currentWidget.deleteLater()
            self.insertWidget(1, ElementView(self, targetName, probeId))
        self.setCurrentIndex(1)

    def setMaxOpenChans(self, num):
        self.maxOpenChans = 3

class WideView(QtGui.QFrame):
    def __init__(self, parent):
        super(WideView, self).__init__(parent)
        self.fr = QtGui.QLabel("WIDEVIEW")
        grid = QtGui.QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)

class ElementView(QtGui.QFrame):
    def __init__(self, parent, targetName, probeId):
        super(ElementView, self).__init__(parent)
        self.fr = QtGui.QLabel(targetName)
        grid = QtGui.QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)



