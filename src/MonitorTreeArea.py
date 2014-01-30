from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    MonitorProxyEvents   import ChannelHandler
import    MonitorDashboardArea
from    NewTargetForm   import  AddTargetWizard
from    CommonWidgets   import  *
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
        self.compositeList = MonitorDashboardList(self)
        self.searchBar  = MonitorTreeSearch(self)
        self.summary    = Summary(self)
        self.info       = MonitorTreeAreaInfo(self)
        self.tabs       = QTabWidget(self)
        self.vServices  = VirtualServices(self)

        self.tabs.addTab(self.treeview,         'Probes')
        self.tabs.addTab(self.compositeList,    'Dashboards')
        self.tabs.addTab(self.vServices,        'Services')

        self.commands = Commands(self)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(5)
        grid.addWidget(self.summary,            0, 0)
        grid.addWidget(self.commands,           1, 0)
        grid.addWidget(self.searchBar,          2, 0)
        grid.addWidget(self.tabs,               3, 0)
        grid.addWidget(self.info,               4, 0)

        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,0)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,0)

        self.setLayout(grid)
        self.setMaximumWidth(500)

class VirtualServices(QFrame):
    def __init__(self, parent):
        super(VirtualServices, self).__init__(parent)
        grid = QGridLayout(self)
        grid.addWidget(QLabel('hello', self), 0,0)
        self.setLayout(grid)

class Commands(QFrame):
    def __init__(self, parent):
        super(Commands, self).__init__(parent)
        grid = QGridLayout(self)
        self.addButton = QPushButton(TkorderIcons.get('list-add'), 'Add', self)
        self.addButton.clicked.connect(self._launchWizard)
        grid.addWidget(self.addButton, 0,0)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        self.setLayout(grid)

    def _launchWizard(self):
        wizard = AddTargetWizard(self)




class MonitorTreeSearch(QFrame):
    def __init__(self, parent):
        super(MonitorTreeSearch, self).__init__(parent)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(0)

        self.line = QLineEdit(self)
        self.line.setPlaceholderText('Filter')
        self.line.textChanged.connect(self.lineTextUpdate)

        clear   = QPushButton(self)
        clear.setIcon(TkorderIcons.get('edit-clear'))
        clear.clicked.connect(self.line.clear)

        grid.addWidget(clear,   0,0)
        grid.addWidget(self.line,    0,1)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        self.setLayout(grid)

    def lineTextUpdate(self):
        text = self.line.text()
        MonitorTreeView.singleton.filterThis(text)


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
### COMPOSITE LISTVIEW #######################################################
##############################################################################
class MonitorDashboardList(QTreeView):
    def __init__(self, parent):
        super(MonitorDashboardList, self).__init__(parent)
        MonitorDashboardList.singleton = self
        self.setAnimated(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHeaderHidden(False)


##############################################################################
### PROBES TREEVIEW ##########################################################
##############################################################################
class MonitorTreeView(QTreeView):
    def __init__(self, parent):
        super(MonitorTreeView, self).__init__(parent)
        MonitorTreeView.singleton = self
        self.model   = MonitorTreeModel(self)
        self.proxy   = QSortFilterProxyModel(self)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setDynamicSortFilter(True)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterRole(Qt.UserRole)
        self.setModel(self.proxy)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setIconSize(QSize(25, 25)) 
        self.setAnimated(True)
        self.setFrameShape(QFrame.NoFrame)
        #self.setHeaderHidden(True)
        self.setObjectName('backTree')
        self.setStyleSheet('QFrame#backTree {   \
            background-image: url(./icons/hover_info_files.png); \
            background-repeat: no-repeat;                            \
            background-attachment: fixed;                            \
            background-position: bottom right}')

        self.createMenus()
        self.contextActions = QAction('test', self)
        self.addAction(self.contextActions)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.test)

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        #self.clicked.connect(self.userActivity)

    def createMenus(self):
        self.targetMenu = QMenu(self)




        targetAction = QAction('Add to working view', self)
        targetAction.triggered[bool].connect(self.addToWorkingView)
        self.targetMenu.addAction(targetAction)


        self.targetMenu.addSeparator()

        targetAction = QAction('Suspend all target probes', self)
        self.targetMenu.addAction(targetAction)

        targetAction = QAction('Create a new probe', self)
        self.targetMenu.addAction(targetAction)
        targetAction.triggered[bool].connect(self.createProbe)

        self.targetMenu.addSeparator()

        targetAction = QAction('Delete this target ans his probes', self)
        self.targetMenu.addAction(targetAction)

        self.targetMenu.addSeparator()

        targetAction = QAction('Properties', self)
        self.targetMenu.addAction(targetAction)


        self.probeMenu  = QMenu(self)

        self.probeMenu.addSeparator()

        probeAction = QAction('Add to working view', self)
        probeAction.triggered[bool].connect(self.addToWorkingView)
        self.probeMenu.addAction(probeAction)

        probeAction = QAction('Suspend probe', self)
        self.probeMenu.addAction(probeAction)

        self.probeMenu.addSeparator()

        probeAction = QAction('Delete this probe', self)
        self.probeMenu.addAction(probeAction)

        self.probeMenu.addSeparator()

        probeAction = QAction('Properties', self)
        self.probeMenu.addAction(probeAction)


        self.noneMenu = QMenu(self)

        noneAction = QAction('Create a new target', self)
        self.noneMenu.addAction(noneAction)
        noneAction.triggered[bool].connect(self.createTarget)

        noneAction = QAction('Select all', self)
        self.noneMenu.addAction(noneAction)


    def createTarget(self): pass
    def createProbe(self): pass
    def configureProbe(self): pass

    def addToWorkingView(self):
        proxyIndexes = self.selectedIndexes()
        selectionList = list()
        for i in range(len(proxyIndexes)):
            modelIndex = self.proxy.mapToSource(proxyIndexes[i])
            modelItem  = self.model.itemFromIndex(modelIndex)
            selectionList.append(modelItem.name)
        MonitorDashboardArea.Dashboard.singleton.userNewSelection(selectionList)

    def userActivity(self, index):
        print "clicked!", self.selectedIndexes()

    def filterThis(self, text):
        self.proxy.setFilterFixedString(text)

    def selectionChanged(self, selected, deselected):
        QTreeView.selectionChanged(self, selected, deselected)

    def test(self, point):
        index = self.proxy.mapToSource(self.indexAt(point))
        item  = self.model.itemFromIndex(index)
        if      item.__class__.__name__ == 'ProbeItem':
            self.probeMenu.popup(self.mapToGlobal(point))
        elif    item.__class__.__name__ == 'TargetItem':
            self.targetMenu.popup(self.mapToGlobal(point))
        elif    item.__class__.__name__ == 'NoneType':
            self.noneMenu.popup(self.mapToGlobal(point))


    def mousePressEvent(self, pressEvent):
        button = pressEvent.button()
        if button == Qt.MouseButton.RightButton: 
            QTreeView.mousePressEvent(self, pressEvent)
        else:
            QTreeView.mousePressEvent(self, pressEvent)


        
class MonitorTreeModel(QStandardItemModel):
    def __init__(self, parent):
        super(MonitorTreeModel, self).__init__(parent)
        self.setHorizontalHeaderLabels(["Targets/Probes"])
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
        self.nodeType   = 'target'
        self.status     = 'UNKNOWN'
        self.searchString   = self.name
        self.targetDict = data
        #self.setFlags(Qt.ItemIsEnabled)
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.name
        elif role == Qt.UserRole:
            return self.searchString
        else:
            return QStandardItem.data(self, role)

    def handleProbeInfo(self, msg):
        count   = self.rowCount()
        probe   = msg['value']['name']
        probeExist = False
        for i in range(count):
            if self.child(i).name == probe:
                child       = self.child(i)
                probeExist  = True
                break

        if probeExist == False:
            self.appendRow(ProbeItem(msg))
        else:
            child.updateState(msg)

        self.searchString = self.name
        for i in range(self.rowCount()):
            self.searchString += self.child(i).name

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
        elif 'OK' in status:
            self.status = 'OK'
            return
        elif 'UNKNOWN' in status:
            self.status = 'UNKNOWN'
            return


class ProbeItem(QStandardItem):
    def __init__(self, data):
        super(ProbeItem, self).__init__()
        self.name       = data['value']['name']
        self.nodeType   = 'probe'
        self.target     = data['value']['target']
        self.status     = data['value']['status']
        self.searchString = self.name + self.target
        self.probeDict = data
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.name
        elif role == Qt.UserRole:
            return self.searchString
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
