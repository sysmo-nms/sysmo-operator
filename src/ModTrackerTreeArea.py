from    PySide.QtCore   import *
from    PySide.QtGui    import *
import  TkorderIcons


#####################################################################
###### LEFT PANNEL VIEW #############################################
#####################################################################
#####################################################################
def handle(msg):
    msgType = msg['msgType']
    if (msgType == 'targetInfo'):
        TrackerTViewModel.handleTargetInfo(msg)
    elif (msgType == 'probeInfo'):
        TrackerTViewModel.handleProbeInfo(msg)
    elif (msgType == 'probeModInfo'):
        TrackerTViewModel.handleProbeModInfo(msg)
    else:
        print "what", msgType

class TreeContainer(QFrame):
    @classmethod
    def toggle(cls):
        if (cls.singleton.isHidden() == True):
            cls.singleton.show()
        else:
            cls.singleton.hide()


    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self.trackerMain  = parent

        self.treeview   =  TrackerTView(self)
        self.treeview.clicked[QModelIndex].connect(TrackerTView.clic)

        # self.filterMenu = QMenu(self)
        # self.filterButton    = QToolButton(self)
        # self.filterButton.setIcon(TkorderIcons.get('Filter'))
        # self.filterButton.setMenu(self.filterMenu)

        # self.configureMenu = QMenu(self)
        # self.configureButton    = QToolButton(self)
        # self.configureButton.setIcon(TkorderIcons.get('preferences-system-session'))
        # self.configureButton.setMenu(self.configureMenu)

        # self.clearButton    = QToolButton(self)
        # self.clearButton.setIcon(TkorderIcons.get('edit-clear'))
        # self.clearButton.setIconSize(QSize(20,20))
        # self.clearButton.setStyleSheet("QToolButton {border: none; padding: 0px; }")

        # self.lineEdit   =   QLineEdit(self)
        # self.lineEdit.setPlaceholderText("Filtrer les sondes")


        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        # grid.addWidget(self.lineEdit,       0, 0)
        # grid.addWidget(self.clearButton,    0, 1)
        # grid.addWidget(self.filterButton,   0, 2)
        # grid.addWidget(self.configureButton,   0, 3)
        # grid.addWidget(self.treeview,       1, 0, 1, 4)
        grid.addWidget(self.treeview,       0, 0)
        self.setLayout(grid)
        self.setMaximumWidth(400)

    def updateEvent(self, event):
        self.trackerMain.updateEvent(event)

class TrackerTView(QTreeView):
    @classmethod
    def set(cls, i):
        cls.tv = i

    @classmethod
    def clic(cls, i):
        model = cls.tv.model()
        item  = model.itemFromIndex(i)
        #TrackerMain.Main.setView(item)
        TreeContainer.singleton.updateEvent(item)
       

    def __init__(self, parent):
        super(TrackerTView, self).__init__(parent)
        TrackerTView.set(self)
        #self.header = QHeaderView(Qt.Horizontal, self)
        #self.header.setClickable(True)
        #self.header.setSortIndicatorShown(True)
        self.setHeaderHidden(True)

        # QTreeview
        self.setAnimated(True)
        #self.setHeader(self.header)
        #Clickabl.setHeaderHidden(True)
        self.setIndentation(15)
        self.setUniformRowHeights(True)
        #self.setRootIsDecorated(False)

        # <- QAbasctractItemView 
        self.setAlternatingRowColors(True)
        self.setDragEnabled(False)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setIconSize(QSize(25, 25)) 
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setModel(TrackerTViewModel(self))

        # <- QAbstractScrollArea
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # <- QFrame
        #self.setFrameShadow(QFrame.Sunken)
        #self.setFrameShape(QFrame.StyledPanel)

        # from QTreeView
        self.expandAll()

class TrackerTViewModel(QStandardItemModel):
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
            flags=Qt.MatchRecursive,
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
        #i2  = icon.pixmap(5,5)
        if infoType == 'create':
            newItem = QStandardItem()
            newItem.setData(channel,    Qt.DisplayRole)
            newItem.setData(icon,       Qt.DecorationRole)
            newItem.setData(itemType,   Qt.UserRole)
            newItem.setData(channel,    Qt.UserRole + 1)
            newItem.setData(properties, Qt.UserRole + 2)
            newItem.setFlags(Qt.ItemIsSelectable)
            newItem.setFlags(Qt.ItemIsEnabled)
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
        if (status == 'OK'):
            icon = TkorderIcons.get('weather-clear')
        elif (status == 'WARNING'):
            icon = TkorderIcons.get('weather-showers')
        elif (status == 'CRITICAL'):
            icon = TkorderIcons.get('weather-severe-alert')
        elif (status == 'UNKNOWN'):
            icon = TkorderIcons.get('weather-few-clouds-night')
        else:
            print "status is ", status
            icon        = TkorderIcons.get('weather-clear-night')

        parentItem = TrackerTViewModel.findTargetByName(parent)
        i = parentItem.rowCount()
        while (i != 0):
            child = parentItem.child(i - 1)
            childId = child.data(Qt.UserRole + 1)
            if (childId == probeId):
                parentItem.removeRow(i - 1)
                break
            i -= 1
        newItem = QStandardItem()
        newItem.setData(name,   Qt.DisplayRole)
        newItem.setData(icon,   Qt.DecorationRole)
        newItem.setData(itemType, Qt.UserRole)
        newItem.setData(pid,    Qt.UserRole + 1)
        newItem.setData(parent, Qt.UserRole + 2)
        newItem.setData(timeout,Qt.UserRole + 3)
        newItem.setData(step,   Qt.UserRole + 4)
        newItem.setData(name,   Qt.UserRole + 5)
        newItem.setData(status, Qt.UserRole + 6)
        newItem.setFlags(Qt.ItemIsSelectable)
        newItem.setFlags(Qt.ItemIsEnabled)

        # temporaire toutes les probes id == 1 propagent leur status
        # au parent
        if (pid == 1):
            parentItem.setData(icon, Qt.DecorationRole)

        parentItem.appendRow(newItem)
