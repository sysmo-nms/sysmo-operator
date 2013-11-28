from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    MonitorEvents   import ChannelHandler
import  TkorderIcons


#####################################################################
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

        self.treeview   = MonitorTreeView(self)
        self.searchBar  = MonitorTreeSearch(self)
        self.info       = MonitorTreeAreaInfo(self)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(5)
        grid.addWidget(self.searchBar,          1, 0)
        grid.addWidget(self.treeview,           2, 0)
        grid.addWidget(self.info,               3, 0)

        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,1)
        grid.setRowStretch(3,0)

        self.setLayout(grid)
        self.setMaximumWidth(500)

class MonitorTreeSearch(QFrame):
    def __init__(self, parent):
        super(MonitorTreeSearch, self).__init__(parent)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(0)
        clear   = QPushButton(self)
        line    = QLineEdit(self)
        clear.setIcon(TkorderIcons.get('edit-clear'))
        line.setPlaceholderText('Filter')
        grid.addWidget(clear,   0,0)
        grid.addWidget(line,    0,1)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        self.setLayout(grid)


class MonitorTreeButtons(QToolBar):
    def __init__(self, parent):
        super(MonitorTreeButtons, self).__init__(parent)
        self.addAction(TkorderIcons.get('applications-development'), 'Debug', self.hello())

    def hello(self): pass

class MonitorTreeAreaInfo(QTextEdit):
    def __init__(self, parent):
        super(MonitorTreeAreaInfo, self).__init__(parent)
        # text document
        dtext   = QTextDocument()
        dtext.setMaximumBlockCount(500)
        tformat = QTextCharFormat()
        tformat.setFontPointSize(8.2)

        # QTextEdit config
        self.setDocument(dtext)
        self.setCurrentCharFormat(tformat)
        self.setReadOnly(True)
        #self.setStyleSheet(
            #"QTextEdit { \
                #border-radius: 10px;\
                #background: #F9EE75 \
            #}")
        self.setFixedHeight(100)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShadow(QFrame.Raised)

        # signals to receive
        sigDict = ChannelHandler.singleton.masterSignalsDict
        sigDict['probeInfo'].signal.connect(self._informational)
        sigDict['targetInfo'].signal.connect(self._informational)
        sigDict['probeModInfo'].signal.connect(self._informational)

    def _informational(self, msg):
        self.append(str(msg))



##############################################################################
### TREEVIEW #################################################################
##############################################################################
class MonitorTreeView(QTreeView):
    def __init__(self, parent):
        super(MonitorTreeView, self).__init__(parent)
        std     = MonitorTreeModel(self)
        self.setModel(std)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setIconSize(QSize(25, 25)) 
        self.setHeaderHidden(True)
        self.setAlternatingRowColors(True)

class MonitorTreeModel(QStandardItemModel):
    def __init__(self, parent):
        super(MonitorTreeModel, self).__init__(parent)
        sigDict = ChannelHandler.singleton.masterSignalsDict
        sigDict['targetInfo'].signal.connect(self._handleTargetInfo)
        sigDict['probeInfo'].signal.connect(self._handleProbeInfo)

    def _handleTargetInfo(self, msg):
        target = self._itemExist(msg['value']['name'])
        if self._itemExist(msg['value']['name']) == []:
            self.appendRow(TargetItem(msg))
        else:
            self._updateRow(target.pop(), msg)

    def _handleProbeInfo(self, msg):
        target = msg['value']['target']
        parent = self._itemExist(target)
        if parent == []:
            self.appendRow(ProbeItem(msg))
        else:
            targetItem = parent.pop()
            targetItem.handleProbeInfo(msg)

    def _updateRow(self, item, msg):
        item.updateState(msg)

    def _itemExist(self, itemName):
        itemList = self.findItems(
            itemName,
            flags  = Qt.MatchRecursive,
            column = 0
        )
        return itemList

class TargetItem(QStandardItem):
    def __init__(self, data):
        super(TargetItem, self).__init__()
        self.name       = data['value']['name']
        self.status     = 'UNKNOWN'
        self.targetDict = data
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.name
        else:
            return QStandardItem.data(self, role)

    def handleProbeInfo(self, msg):
        count   = self.rowCount()
        probe   = msg['value']['name']
        probeExist = False
        for i in range(count):
            if self.child(i).name == probe:
                probeExist  = True
                child       = self.child(i)
                break

        if probeExist == False:
            self.appendRow(ProbeItem(msg))
        else:
            child.updateState(msg)
        self._setWorstStatus()
        self.emitDataChanged()

    def updateState(self, msg):
        self.targetDict = msg

    def __lt__(self, other): pass

    def _getIconStatus(self):
        if self.status  == 'UNKNOWN':
            return TkorderIcons.get('weather-clear-night')
        elif self.status == 'WARNING':
            return TkorderIcons.get('weather-showers')
        elif self.status == 'CRITICAL':
            return TkorderIcons.get('weather-severe-alert')
        elif self.status == 'OK':
            return TkorderIcons.get('weather-clear')

    def _setWorstStatus(self):
        count = self.rowCount()
        status = list()
        for i in range(count):
            probe = self.child(i)
            status.append(probe.status)

        if 'CRITICAL' in status:
            self.status = 'CRITICAL'
            return
        elif 'WARNING' in status:
            self.status = 'WARNING'
            return
        elif 'UNKNOWN' in status:
            self.status = 'UNKNOWN'
            return
        elif 'OK' in status:
            self.status = 'OK'
            return


class ProbeItem(QStandardItem):
    def __init__(self, data):
        super(ProbeItem, self).__init__()
        self.name   = data['value']['name']
        self.target = data['value']['target']
        self.status = data['value']['status']
        self.probeDict = data
        print self.flags()
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.name
        elif role == Qt.EditRole:
            return None
        else:
            return QStandardItem.data(self, role)

    def updateState(self, data):
        self.status     = data['value']['status']
        self.probeDict  = data
        self.emitDataChanged()

    def __lt__(self, other): pass

    def _getIconStatus(self):
        if self.status == 'UNKNOWN':
            return TkorderIcons.get('weather-clear-night')
        if self.status == 'WARNING':
            return TkorderIcons.get('weather-showers')
        if self.status == 'CRITICAL':
            return TkorderIcons.get('weather-severe-alert')
        if self.status == 'OK':
            return TkorderIcons.get('weather-clear')



# class MonitorTreeView(QTreeView):
#     def __init__(self, parent):
#         super(MonitorTreeView, self).__init__(parent)
#         # MonitorTreeView.singleton = self
#         targetModel = MonitorTreeViewModel(self)
#         self.setSelectionMode(QAbstractItemView.ExtendedSelection)
#         self.setModel(targetModel)
# 
#         #self.setHeaderHidden(True)
#         #self.setAnimated(True)
#         #self.setIndentation(15)
#         #self.setUniformRowHeights(True)
# 
#         # <- QAbasctractItemView 
#         #self.setAlternatingRowColors(True)
#         #self.setDragEnabled(False)
#         #self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
#         #self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
#         #self.setIconSize(QSize(25, 25)) 
#         #self.setSelectionBehavior(QAbstractItemView.SelectItems)
# 
#         # <- QAbstractScrollArea
#         #self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
#         #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
# 
#         # from QTreeView
#         #self.expandAll()
# 
#         # slots
#         # self.selectionChanged.connect(self._userSelection)
# 
#     def selectionChanged(self, selected, deselected):
#         print selected, deselected
#         QTreeView.selectionChanged(self, selected, deselected)
# 
#     #def userClic(self, index):
#         #item    = self.targetModel.itemFromIndex(index)
#         #parent  = item.parent()
#         #emitDict = dict()
# 
#         #if isinstance(parent, QStandardItem):
#             #emitDict['target']  = parent.data(Qt.DisplayRole)
#             #emitDict['probeId'] = item.data(Qt.DisplayRole)
#         #else:
#             #emitDict['target']  = item.data(Qt.DisplayRole)
#             #emitDict['probeId'] = None
#         #MonitorEvents.singleton.treeviewClicked.emit(emitDict)
# 
# 
# class MonitorTreeViewModel(QStandardItemModel):
#     def __init__(self, parent):
#         super(MonitorTreeViewModel, self).__init__(parent)
#         #MonitorTreeViewModel.singleton = self
#         #parentItem = self.invisibleRootItem()
# 
#         # QStandardItemModel
#         self.setColumnCount(1)
#         self.setHorizontalHeaderLabels(['Targets/Probes'])
# 
#         # signals to receive
#         sigDict = ChannelHandler.singleton.masterSignalsDict
#         sigDict['probeInfo'].signal.connect(self._handleProbeInfo)
#         sigDict['targetInfo'].signal.connect(self._handleTargetInfo)
#         sigDict['probeModInfo'].signal.connect(self._handleProbeModInfo)
# 
#     def findTargetByName(self, targetName):
#         parentItemList = self.findItems(
#             targetName,
#             flags=Qt.MatchRecursive,
#             column=0
#         )
#         parentItem = parentItemList.pop()
#         return parentItem
# 
#     def _handleProbeModInfo(self, msg): pass
# 
#     def _handleTargetInfo(self, msg):
#         val         = msg['value']
#         name        = val['name']
#         infoType    = val['infoType']
#         properties  = val['properties']
#         itemType    = 'target'
#         icon        = TkorderIcons.get('weather-clear-night')
#         #i2  = icon.pixmap(5,5)
#         if infoType == 'create':
#             newItem = QStandardItem()
#             newItem.setEnabled(True)
#             print newItem.flags()
#             newItem.setFlags(Qt.ItemIsSelectable)
#             newItem.setData(name,    Qt.DisplayRole)
#             newItem.setData(icon,       Qt.DecorationRole)
#             newItem.setData(itemType,   Qt.UserRole)
#             newItem.setData(name,    Qt.UserRole + 1)
#             newItem.setData(properties, Qt.UserRole + 2)
#             newItem.setFlags(Qt.ItemIsSelectable)
#             newItem.setFlags(Qt.ItemIsEnabled)
#             self.appendRow(newItem)
#             #self.elements.sortChildren(0)
# 
#     def _handleProbeInfo(self, msg):
#         val         = msg['value']
#         parent      = val['target']
#         name        = val['name']
#         probeId     = val['id']
#         status      = val['status']
#         timeout     = val['timeout']
#         step        = val['step']
#         pid         = val['id']
#         itemType    = 'probe'
#         if (status == 'OK'):
#             icon = TkorderIcons.get('weather-clear')
#         elif (status == 'WARNING'):
#             icon = TkorderIcons.get('weather-showers')
#         elif (status == 'CRITICAL'):
#             icon = TkorderIcons.get('weather-severe-alert')
#         elif (status == 'UNKNOWN'):
#             icon = TkorderIcons.get('weather-few-clouds-night')
#         else:
#             print "status is ", status
#             icon        = TkorderIcons.get('weather-clear-night')
# 
#         parentItem = self.findTargetByName(parent)
#         i = parentItem.rowCount()
#         while (i != 0):
#             child = parentItem.child(i - 1)
#             childId = child.data(Qt.UserRole + 1)
#             if (childId == probeId):
#                 parentItem.removeRow(i - 1)
#                 break
#             i -= 1
# 
#         newItem = ProbeItem()
#         newItem.setEnabled(True)
#         newItem.setSelectable(True)
#         newItem.setData(name,   Qt.DisplayRole)
#         newItem.setData(icon,   Qt.DecorationRole)
#         newItem.setData(itemType, Qt.UserRole)
#         newItem.setData(pid,    Qt.UserRole + 1)
#         newItem.setData(parent, Qt.UserRole + 2)
#         newItem.setData(timeout,Qt.UserRole + 3)
#         newItem.setData(step,   Qt.UserRole + 4)
#         newItem.setData(name,   Qt.UserRole + 5)
#         newItem.setData(status, Qt.UserRole + 6)
#         newItem.setFlags(Qt.ItemIsSelectable)
#         newItem.setFlags(Qt.ItemIsEnabled)
# 
#         # temporaire toutes les probes id == 1 propagent leur status
#         # au parent
#         if (pid == 1):
#             parentItem.setData(icon, Qt.DecorationRole)
# 
#         parentItem.appendRow(newItem)
# 
# class ProbeItem(QStandardItem):
#     def __init__(self):
#         super(ProbeItem, self).__init__()
# 
# 
#     def data(self, role):
#         pass
