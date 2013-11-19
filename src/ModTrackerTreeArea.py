from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    ModTrackerEvents    import TrackerEvents
import  TkorderIcons


#####################################################################
###### LEFT PANNEL VIEW #############################################
#####################################################################
#####################################################################
class TreeContainer(QFrame):
    
    " the left tree area. Emit user clics events"

    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self.trackerMain  = parent

        self.treeview   =  TrackerTView(self)
        #self.treeview.clicked[QModelIndex].connect(TrackerTView.singleton.clic)

        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        self.info = TrackerTreeAreaInfo(self)
        grid.addWidget(self.treeview,           0, 0)
        grid.addWidget(self.info,               1, 0)
        self.setLayout(grid)
        self.setMaximumWidth(500)

    def updateEvent(self, event):
        self.trackerMain.updateEvent(event)


class TrackerTreeAreaInfo(QTextEdit):
    def __init__(self, parent):
        super(TrackerTreeAreaInfo, self).__init__(parent)
        dtext   = QTextDocument()
        dtext.setMaximumBlockCount(500)
        tformat = QTextCharFormat()
        tformat.setFontPointSize(8.2)
        self.setDocument(dtext)
        self.setCurrentCharFormat(tformat)
        self.setReadOnly(True)
        self.setStyleSheet(
            "QTextEdit { \
                border: none;\
                border-radius: 0px;\
                background: #F9EE75 \
            }")
        self.setFixedHeight(100)
        TrackerEvents.singleton.probeInfo.connect(self.probeInfoMsg)
        TrackerEvents.singleton.targetInfo.connect(self.targetInfoMsg)
        TrackerEvents.singleton.probeDump.connect(self.probeDumpMsg)
        TrackerEvents.singleton.probeModInfo.connect(self.probeModInfo)
        TrackerEvents.singleton.probeReturn.connect(self.probeModInfo)
        TrackerEvents.singleton.probeActivity.connect(self.probeModInfo)
        TrackerEvents.singleton.subscribeOk.connect(self.probeModInfo)
        TrackerEvents.singleton.unsubscribeOk.connect(self.probeModInfo)

    def probeDumpMsg(self, msg):
        self.append("probe dump")

    def probeInfoMsg(self, msg):
        self.append(str(msg))

    def targetInfoMsg(self, msg):
        self.append(str(msg))

    def probeModInfo(self, msg):
        self.append(str(msg))

    def subscribeOk(self, msg):
        self.append(str(msg))

    def unsubscribeOk(self, msg):
        self.append(str(msg))

    def probeReturn(self, msg):
        self.append(str(msg))

    def probeActivity(self, msg):
        self.append(str(msg))



############
# Treeview #
############
class TrackerTView(QTreeView):
    def __init__(self, parent):
        super(TrackerTView, self).__init__(parent)
        TrackerTView.singleton = self
        self.setHeaderHidden(True)

        self.setAnimated(True)
        self.setIndentation(15)
        self.setUniformRowHeights(True)

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

        # from QTreeView
        self.expandAll()

    #def clic(self, i):
        #print "clic"
        #model = self.model()
        #item  = model.itemFromIndex(i)
        #TreeContainer.singleton.updateEvent(item)


class TrackerTViewModel(QStandardItemModel):

    def __init__(self, parent):
        super(TrackerTViewModel, self).__init__(parent)
        parentItem      = self.invisibleRootItem()

        # QStandardItemModel
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels([''])
        TrackerTViewModel.singleton = self

        TrackerEvents.singleton.probeModInfo.connect(self.handleProbeModInfo)
        TrackerEvents.singleton.probeInfo.connect(self.handleProbeInfo)
        TrackerEvents.singleton.targetInfo.connect(self.handleTargetInfo)

    def findTargetByName(self, targetName):
        parentItemList = self.findItems(
            targetName,
            flags=Qt.MatchRecursive,
            column=0
        )
        parentItem = parentItemList.pop()
        return parentItem

    def handleProbeModInfo(self, msg): pass

    def handleTargetInfo(self, msg):
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

    def handleProbeInfo(self, msg):
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

        parentItem = self.findTargetByName(parent)
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

