from    PySide.QtCore   import *
from    PySide.QtGui    import *

import nocapi
from    noctopus_widgets        import (
    NFrame,
    NFrameContainer,
    NGrid,
    NGridContainer
)
from    opus.monitor.widgets    import  *

class ProbesTree(NFrame):
    def __init__(self, parent):
        super(ProbesTree, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self._grid = NGrid(self)
        self._probesActions     = ProbesActions(self)
        self._probesTreeview    = ProbesTreeview(self)
        self._grid.addWidget(self._probesActions,   0,0)
        self._grid.addWidget(self._probesTreeview,  1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

class ProbesTreeview(QTreeView):
    def __init__(self, parent):
        super(ProbesTreeview, self).__init__(parent)
        ProbesTree.singleton = self
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
        #self.setFrameShape(QFrame.NoFrame)
        #self.setHeaderHidden(True)
        self.setObjectName('backTree')
        self.setStyleSheet('''QFrame#backTree { 
            background-image: url(./graphics/hover_info_files.png);
            background-repeat: no-repeat;
            background-attachment: fixed; 
            background-position: bottom right}''')

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

        localMenu    = QMenu('Local Actions', self)
        sshAction = QAction('Acces SSH', self)
        phpAction = QAction('Acces phpldapadmin HTTP', self)
        configureAction = QAction('Configure new action', self)
        localMenu.addAction(sshAction)
        localMenu.addAction(phpAction)
        localMenu.addSeparator()
        localMenu.addAction(configureAction)

        self.targetMenu.addMenu(localMenu)

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

        probeAction = QAction('Force check', self)
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
        #MonitorDashboardArea.Dashboard.singleton.userNewSelection(selectionList)

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
        #sigDict = ChannelHandler.singleton.masterSignalsDict
        #sigDict['targetInfo'].signal.connect(self._handleTargetInfo)
        #sigDict['probeInfo'].signal.connect(self._handleProbeInfo)

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

class ProbesActions(NFrameContainer):
    def __init__(self, parent):
        super(ProbesActions, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)

        self._line = QLineEdit(self)
        self._line.setPlaceholderText('Filter')
        self._line.textChanged.connect(self._lineChanged)

        add   = QPushButton(self)
        add.setIcon(nocapi.nGetIcon('list-add'))

        clear = QPushButton(self)
        clear.setIcon(nocapi.nGetIcon('edit-clear'))
        clear.clicked.connect(self._line.clear)

        grid.addWidget(add,         0,0)
        grid.addWidget(clear,       0,1)
        grid.addWidget(self._line,  0,2)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)
        self.setLayout(grid)

    def _lineChanged(self):
        text = self._line.text()
        print text
        #MonitorTreeview.singleton.filterThis(text)
