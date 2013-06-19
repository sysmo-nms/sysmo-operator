from PySide import QtGui, QtCore
import ModTrackerIcons
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
        self.connect(
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
    def __init__(self, parent):
        super(TrackerTView, self).__init__(parent)
        self.header = QtGui.QHeaderView(QtCore.Qt.Horizontal, self)

        #
        # QTreeview
        self.setAnimated(True)
        #self.setHeaderHidden(True)
        self.setIndentation(15)
        self.setUniformRowHeights(True)
        self.expandAll()
        #self.setRootIsDecorated(False)

        # <- QAbasctractItemView 
        self.setModel(TrackerTViewModel(self))
        self.setAlternatingRowColors(True)
        self.setDragEnabled(False)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        # self.setIconSize(size) !!!! j en veux plusieurs moi
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        # <- QAbstractScrollArea
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # <- QFrame
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setFrameShape(QtGui.QFrame.StyledPanel)

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
        cls.tvm.pModInfo(msg)

    def __init__(self, parent):
        super(TrackerTViewModel, self).__init__(parent)
        parentItem      = self.invisibleRootItem()
        self.elements   = QtGui.QStandardItem("Elements")
        self.views      = QtGui.QStandardItem("Views")
        self.probes     = QtGui.QStandardItem("Probes")

        # QStandardItemModel
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(['Class/Elements'])
        #self.setHorizontalHeaderItem(0, QtGui.QStandardItem('jlk'))
        #self.setVerticalHeaderItem(0, QtGui.QStandardItem('jlk'))
        #self.setVerticalHeaderLabels(['jj/fjsdlk'])

        self.elements.setFlags(QtCore.Qt.ItemIsEnabled)
        self.views.setFlags(QtCore.Qt.ItemIsEnabled)
        self.probes.setFlags(QtCore.Qt.ItemIsEnabled)


        parentItem.appendRows([self.elements,self.views,self.probes])

        TrackerTViewModel.setTVM(self)

    def pModInfo(self, msg):
        val     = msg['value']
        info    = val['info']
        name    = val['name']
        newItem = QtGui.QStandardItem(name)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable)
        newItem.setFlags(QtCore.Qt.ItemIsEnabled)

        self.probes.appendRow(newItem)

    def tInfo(self, msg):
        val     = msg['value']
        channel = val['channel']
        infoType = val['infoType']
        if infoType == 'create':
            newItem = QtGui.QStandardItem(channel)
            newItem.setFlags(QtCore.Qt.ItemIsSelectable)
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.elements.appendRow(newItem)
            self.elements.sortChildren(0)

    def pInfo(self, msg):
        val     = msg['value']
        parent  = val['channel']
        name    = val['name']
        probeId = val['id']

        parentItemList = self.findItems(
            parent,
            flags=QtCore.Qt.MatchRecursive,
            column=0
        )
        parentItem = parentItemList.pop()
        newItem = QtGui.QStandardItem(name)
        newItem.setFlags(QtCore.Qt.ItemIsSelectable)
        newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        parentItem.appendRow(newItem)


