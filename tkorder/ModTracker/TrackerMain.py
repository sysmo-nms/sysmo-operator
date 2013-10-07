from    PySide import QtGui, QtCore
import  TkorderIcons
import  TkorderMain
import  PowerTree

class TrackerWindow(QtGui.QSplitter):
    @classmethod
    def setMyself(cls, myself):
        cls.myself = myself

    @classmethod
    def myself(cls):
        return cls.myself

    @classmethod
    def initView(cls):
        stack = cls.myself.rightStack
        stack.addWidget(WideView(cls.myself))

    @classmethod
    def setView(cls, item):
        if   item.data(QtCore.Qt.UserRole) == 'target':
            target  = item
            probeId = None 
        elif item.data(QtCore.Qt.UserRole) == 'probe':
            target = PowerTree.TrackerTViewModel.findTargetByName(item.data(QtCore.Qt.UserRole + 2))
            probeId = item.data(QtCore.Qt.UserRole + 1)

        rightStack = cls.myself.rightStack
        rightStack.setView(target, probeId)

    @classmethod
    def setMaxOpenStacks(cls, num):
        cls.maxOpenStacks = num

    def __init__(self, parent):
        super(TrackerWindow, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        sin = TkorderMain.SupercastClient.singleton
        sin.setMessageProcessor('modTrackerPDU', self.handleMsg)

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
            PowerTree.TrackerTViewModel.handleProbeInfo(msg)
        elif (mType == 'targetInfo'):
            print "received targetInfo"
            PowerTree.TrackerTViewModel.handleTargetInfo(msg)
        elif (mType == 'probeModInfo'):
            print "received probeModInfo"
            PowerTree.TrackerTViewModel.handleProbeModInfo(msg)
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
