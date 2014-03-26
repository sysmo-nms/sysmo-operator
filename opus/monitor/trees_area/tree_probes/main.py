from    PySide.QtCore   import (
    Qt,
    QSize
)

from    PySide.QtGui    import (
    QTreeView,
    QFrame,
    QSortFilterProxyModel,
    QAbstractItemView,
    QMenu,
    QAction
)

from    noctopus_widgets    import (
    NFrame,
    NGrid
)

from    opus.monitor.trees_area.tree_probes.controls import ProbesActions
from    opus.monitor.trees_area.tree_probes.model    import ProbeModel
import  nocapi

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
        self._initStyle()
        self.model   = ProbeModel(self)
        self.proxy   = QSortFilterProxyModel(self)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setDynamicSortFilter(True)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterRole(Qt.UserRole)
        self.setModel(self.proxy)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self._initMenus()
        self.contextActions = QAction('test', self)
        self.addAction(self.contextActions)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.test)

        self.setSortingEnabled(True)

    def _initStyle(self):
        self.setObjectName('backTree')
        self.setIconSize(QSize(25, 25)) 
        self.setAnimated(True)
        self.setAlternatingRowColors(True)
        self.setStyleSheet('''QFrame#backTree { 
            background-image: url(./graphics/hover_info_files.png);
            background-repeat: no-repeat;
            background-color: %s;
            background-attachment: fixed; 
            background-position: bottom right}''' % nocapi.nGetRgb('Base'))

    def _initMenus(self):
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
