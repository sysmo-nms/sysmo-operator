from PySide import QtGui, QtCore
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
        self.button      =  QtGui.QPushButton("toggle left")
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
        self.setModel(TrackerTViewModel())


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

    def __init__(self):
        super(TrackerTViewModel, self).__init__()
        parentItem  = self.invisibleRootItem()
        self.elements    = QtGui.QStandardItem("Elements")
        self.views       = QtGui.QStandardItem("Views")
        self.probes      = QtGui.QStandardItem("Probes")
        parentItem.appendRows([self.elements,self.views,self.probes])
        TrackerTViewModel.setTVM(self)

    def pModInfo(self, msg):
        val     = msg['value']
        info    = val['info']
        name    = val['name']
        #probesRoot = self.findItems(
            #"Probes", 
            #flags=QtCore.Qt.MatchExactly,
            #column=0
        #)
        self.probes.appendRow(QtGui.QStandardItem(name))

    def tInfo(self, msg):
        val     = msg['value']
        channel = val['channel']
        infoType = val['infoType']
        if infoType == 'create':
            self.elements.appendRow(QtGui.QStandardItem(channel))
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
        parentItem.appendRow(QtGui.QStandardItem(name))


