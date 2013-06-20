from PySide import QtGui, QtCore
import TkorderIcons
import TkorderMain

class ModTracker(QtGui.QSplitter):
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
            target = TrackerTViewModel.findTargetByName(item.data(QtCore.Qt.UserRole + 2))
            probeId = item.data(QtCore.Qt.UserRole + 1)

        rightStack = cls.myself.rightStack
        rightStack.setView(target, probeId)

    @classmethod
    def setMaxOpenStacks(cls, num):
        cls.maxOpenStacks = num

    def __init__(self, parent):
        super(ModTracker, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        sin = TkorderMain.SupercastClient.singleton
        sin.setMessageProcessor('modTrackerPDU', self.handleMsg)

        self.leftTree   = LeftPane(self)
        self.rightStack = RightPane(self)
        self.rightStack.setMaxOpenChans(3)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightStack)
        
        ModTracker.setMyself(self)
        ModTracker.initView()

    def handleMsg(self, msg):
        mType = msg['msgType']

        if   (mType == 'probeInfo'):
            TrackerTViewModel.handleProbeInfo(msg)
        elif (mType == 'targetInfo'):
            TrackerTViewModel.handleTargetInfo(msg)
        elif (mType == 'probeModInfo'):
            TrackerTViewModel.handleProbeModInfo(msg)
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


#####################################################################
#####################################################################
###### LEFT PANNEL VIEW #############################################
#####################################################################
#####################################################################
class LeftPane(QtGui.QFrame):
    @classmethod
    def setSingleton(cls, obj):
        cls.singleton = obj

    @classmethod
    def singleton(cls):
        return cls.singleton

    @classmethod
    def toggle(cls):
        if (cls.singleton.isHidden() == True):
            cls.singleton.show()
        else:
            cls.singleton.hide()


    def __init__(self, parent):
        super(LeftPane, self).__init__(parent)
        LeftPane.setSingleton(self)
        self.treeview   =  TrackerTView(self)
        self.treeview.clicked[QtCore.QModelIndex].connect(TrackerTView.clic)

        self.button     =  QtGui.QPushButton("left here", self)
        grid = QtGui.QGridLayout()
        grid.addWidget(self.button,   0, 0)
        grid.addWidget(self.treeview, 1, 0)
        self.setLayout(grid)

class TrackerTView(QtGui.QTreeView):
    @classmethod
    def set(cls, i):
        cls.tv = i

    @classmethod
    def clic(cls, i):
        model = cls.tv.model()
        item  = model.itemFromIndex(i)
        ModTracker.setView(item)

    def __init__(self, parent):
        super(TrackerTView, self).__init__(parent)
        TrackerTView.set(self)
        self.header = QtGui.QHeaderView(QtCore.Qt.Horizontal, self)

        # QTreeview
        self.setAnimated(True)
        self.setHeaderHidden(True)
        self.setIndentation(15)
        self.setUniformRowHeights(True)
        #self.setRootIsDecorated(False)

        # <- QAbasctractItemView 
        self.setAlternatingRowColors(True)
        self.setDragEnabled(False)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setIconSize(QtCore.QSize(30, 30)) #!!!! j en veux plusieurs moi
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setModel(TrackerTViewModel(self))

        # <- QAbstractScrollArea
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # <- QFrame
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setFrameShape(QtGui.QFrame.StyledPanel)

        # from QTreeView
        self.expandAll()

class TrackerTViewModel(QtGui.QStandardItemModel):
    @classmethod
    def setTVM(cls, i):
        cls.tvm  = i

    @classmethod
    def handleTargetInfo(cls, msg):
        cls.tvm.tInfo(msg)

    @classmethod
    def handleProbeInfo(cls, msg):
        cls.tvm.pInfo(msg)

    @classmethod
    def handleProbeModInfo(cls, msg):
        return

    @classmethod
    def findTargetByName(cls, targetName):
        tv = cls.tvm
        parentItemList = tv.findItems(
            targetName,
            flags=QtCore.Qt.MatchRecursive,
            column=0
        )
        parentItem = parentItemList.pop()
        return parentItem

    def __init__(self, parent):
        super(TrackerTViewModel, self).__init__(parent)
        parentItem      = self.invisibleRootItem()

        # QStandardItemModel
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels([''])
        TrackerTViewModel.setTVM(self)

    def tInfo(self, msg):
        val         = msg['value']
        channel     = val['channel']
        infoType    = val['infoType']
        properties  = val['properties']
        itemType    = 'target'
        icon        = TkorderIcons.get('weather-clear-night')
        i2  = icon.pixmap(5,5)
        if infoType == 'create':
            newItem = QtGui.QStandardItem()
            newItem.setData(channel,    QtCore.Qt.DisplayRole)
            newItem.setData(icon,       QtCore.Qt.DecorationRole)
            newItem.setData(itemType,   QtCore.Qt.UserRole)
            newItem.setData(channel,    QtCore.Qt.UserRole + 1)
            newItem.setData(properties, QtCore.Qt.UserRole + 2)
            newItem.setFlags(QtCore.Qt.ItemIsSelectable)
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.appendRow(newItem)
            #self.elements.sortChildren(0)

    def pInfo(self, msg):
        val         = msg['value']
        parent      = val['channel']
        name        = val['name']
        probeId     = val['id']
        status      = val['status']
        timeout     = val['timeout']
        step        = val['step']
        pid         = val['id']
        itemType    = 'probe'
        icon        = TkorderIcons.get('weather-clear-night')
        #parentItemList = self.findItems(
            #parent,
            #flags=QtCore.Qt.MatchRecursive,
            #column=0
        #)
        #parentItem = parentItemList.pop()
        parentItem = TrackerTViewModel.findTargetByName(parent)
        newItem = QtGui.QStandardItem()
        newItem.setData(name,   QtCore.Qt.DisplayRole)
        newItem.setData(icon,   QtCore.Qt.DecorationRole)
        newItem.setData(itemType, QtCore.Qt.UserRole)
        newItem.setData(pid,    QtCore.Qt.UserRole + 1)
        newItem.setData(parent, QtCore.Qt.UserRole + 2)
        newItem.setData(timeout,QtCore.Qt.UserRole + 3)
        newItem.setData(step,   QtCore.Qt.UserRole + 4)
        newItem.setData(name,   QtCore.Qt.UserRole + 5)
        newItem.setData(status, QtCore.Qt.UserRole + 6)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable)
        newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        parentItem.appendRow(newItem)
