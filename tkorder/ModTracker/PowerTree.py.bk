from    PySide import QtGui, QtCore
import  TkorderIcons
import  TrackerMain


#####################################################################
###### LEFT PANNEL VIEW #############################################
#####################################################################
#####################################################################
class PowerTreeContainer(QtGui.QFrame):
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
        super(PowerTreeContainer, self).__init__(parent)
        PowerTreeContainer.setSingleton(self)
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
        TrackerMain.TrackerWindow.setView(item)

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
