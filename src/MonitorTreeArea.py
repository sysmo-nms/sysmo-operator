from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    MonitorEvents   import ChannelHandler
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

        self.treeview   = MonitorTView(self)
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



class MonitorTView(QTableView):
    def __init__(self, parent):
        super(MonitorTView, self).__init__(parent)
        self.setModel(MyModel(self))

class MyModel(QAbstractTableModel):
    def __init__(self, parent):
        super(MyModel, self).__init__(parent)
        self.time = QTime()
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.timerHit)
        timer.start()
        
    def timerHit(self):
        print "timer hit"
        index = self.createIndex(2,0)
        self.dataChanged.emit(index, index)
        
    def rowCount(self, parent = QModelIndex()):
        return 3

    def columnCount(self, parent = QModelIndex()):
        return 3

    def headerData(self, section, orient, role):
        if role == Qt.DisplayRole:
            if orient == Qt.Horizontal:
                if section == 0:
                    return u'un'
                elif section == 1:
                    return u'deux'
                elif section == 2:
                    return u'trois'

    def data(self, index, role):
        row = index.row()
        col = index.column()
        print "."
        if role == Qt.DisplayRole:
            if row == 2 and col == 0:
                t = self.time.currentTime()
                return t.toString()
            else:
                return  "row %i, column %i" % (index.row(), index.column())
        elif role == Qt.FontRole:
            if row == 0 and col == 0:
                f = QFont()
                f.setBold(True)
                return f
        elif role == Qt.BackgroundRole:
            if row == 1 and col == 1:
                c = QColor(255,0,0)
                return c
        elif role == Qt.TextAlignmentRole:
            if row == 1 and col == 0:
                return Qt.AlignRight
        elif role == Qt.CheckStateRole:
            if row == 0 and col == 1:
                return Qt.Checked


############
# Treeview #
############
# class MonitorTView(QTreeView):
#     def __init__(self, parent):
#         super(MonitorTView, self).__init__(parent)
#         MonitorTView.singleton = self
#         self.targetModel = MonitorTViewModel(self)
# 
#         self.setHeaderHidden(True)
#         self.setAnimated(True)
#         self.setIndentation(15)
#         self.setUniformRowHeights(True)
# 
#         # <- QAbasctractItemView 
#         self.setModel(self.targetModel)
#         self.setAlternatingRowColors(True)
#         self.setDragEnabled(False)
#         self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
#         self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
#         self.setIconSize(QSize(25, 25)) 
#         self.setSelectionMode(QAbstractItemView.ExtendedSelection)
#         self.setSelectionBehavior(QAbstractItemView.SelectItems)
# 
#         # <- QAbstractScrollArea
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
# 
#         # from QTreeView
#         self.expandAll()
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
# class MonitorTViewModel(QStandardItemModel):
# 
#     def __init__(self, parent):
#         super(MonitorTViewModel, self).__init__(parent)
#         MonitorTViewModel.singleton = self
#         parentItem      = self.invisibleRootItem()
# 
#         # QStandardItemModel
#         self.setColumnCount(1)
#         self.setHorizontalHeaderLabels([''])
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
#         channel     = val['channel']
#         infoType    = val['infoType']
#         properties  = val['properties']
#         itemType    = 'target'
#         icon        = TkorderIcons.get('weather-clear-night')
#         #i2  = icon.pixmap(5,5)
#         if infoType == 'create':
#             newItem = QStandardItem()
#             newItem.setData(channel,    Qt.DisplayRole)
#             newItem.setData(icon,       Qt.DecorationRole)
#             newItem.setData(itemType,   Qt.UserRole)
#             newItem.setData(channel,    Qt.UserRole + 1)
#             newItem.setData(properties, Qt.UserRole + 2)
#             newItem.setFlags(Qt.ItemIsSelectable)
#             newItem.setFlags(Qt.ItemIsEnabled)
#             self.appendRow(newItem)
#             #self.elements.sortChildren(0)
# 
#     def _handleProbeInfo(self, msg):
#         val         = msg['value']
#         parent      = val['channel']
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
#         newItem = QStandardItem()
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
