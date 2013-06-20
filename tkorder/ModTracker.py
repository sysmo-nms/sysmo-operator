from PySide import QtGui, QtCore
import TkorderIcons
import TkorderMain

class ModTracker(QtGui.QSplitter):
    @classmethod
    def initTargetView(cls):
        cls.targetView = ''

    @classmethod
    def targetView(cls):
        return cls.targetView

    def __init__(self, parent):
        super(ModTracker, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        sin = TkorderMain.SupercastClient.singleton
        sin.setMessageProcessor('modTrackerPDU', self.handleMsg)

        self.addWidget(LeftPane(self))
        self.addWidget(RightPane(self))

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


class RightPane(QtGui.QFrame):
    def __init__(self, parent):
        super(RightPane, self).__init__(parent)
        self.button = QtGui.QPushButton("toggle left")
        grid = QtGui.QGridLayout()
        grid.addWidget(self.button,   0, 0)
        self.setLayout(grid)
        QtCore.QObject.connect(
            self.button,
            QtCore.SIGNAL("clicked()"),
            LeftPane.toggle
        )


#####################################################################
#####################################################################
###### TREEVIEW MODEL ###############################################
#####################################################################
#####################################################################
class TrackerTView(QtGui.QTreeView):
    @classmethod
    def set(cls, i):
        cls.tv = i

    @classmethod
    def clic(cls, i):
        model = cls.tv.model()
        item  = model.itemFromIndex(i)

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
        icon        = TkorderIcons.get('weather-clear-night')
        i2  = icon.pixmap(5,5)
        if infoType == 'create':
            newItem = QtGui.QStandardItem()
            newItem.setData(channel,    QtCore.Qt.DisplayRole)
            newItem.setData(icon,       QtCore.Qt.DecorationRole)
            newItem.setData(properties, QtCore.Qt.UserRole)
            newItem.setFlags(QtCore.Qt.ItemIsSelectable)
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.appendRow(newItem)
            #self.elements.sortChildren(0)

    def pInfo(self, msg):
        val     = msg['value']
        parent  = val['channel']
        name    = val['name']
        probeId = val['id']
        status  = val['status']
        timeout = val['timeout']
        step    = val['step']
        pid     = val['id']
        icon    = TkorderIcons.get('weather-clear-night')
        parentItemList = self.findItems(
            parent,
            flags=QtCore.Qt.MatchRecursive,
            column=0
        )
        parentItem = parentItemList.pop()
        newItem = QtGui.QStandardItem()
        newItem.setData(name,   QtCore.Qt.DisplayRole)
        newItem.setData(icon,   QtCore.Qt.DecorationRole)
        newItem.setData(status, QtCore.Qt.UserRole)
        newItem.setData(timeout,QtCore.Qt.UserRole + 1)
        newItem.setData(step,   QtCore.Qt.UserRole + 2)
        newItem.setData(pid,    QtCore.Qt.UserRole + 3)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable)
        newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        parentItem.appendRow(newItem)
