from    PySide.QtCore   import (
    Qt,
    QSize
)

from    PySide.QtGui    import (
    QTreeView,
    QHeaderView,
    QFrame,
    QSortFilterProxyModel,
    QAbstractItemView,
    QMenu,
    QAction,
    QStyledItemDelegate,
    QStyleOptionProgressBar,
    QApplication,
    QStyle,
    QImage,
)

from    noctopus_widgets    import (
    NFrame,
    NGrid
)

from    functools import partial
from    opus.monitor.trees_area.tree_probes.controls import ProbesActions
from    opus.monitor.trees_area.tree_probes.model    import ProbeModel
from    opus.monitor.trees_area.tree_probes.logwin   import LoggerView
import  opus.monitor.api    as monapi
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
        ProbesTreeview.singleton = self
        self._viewDialogs = dict()
        self._initStyle()
        self.model   = ProbeModel(self)
        self.proxy   = QSortFilterProxyModel(self)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setDynamicSortFilter(True)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterRole(Qt.UserRole)
        self.setModel(self.proxy)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setDropIndicatorShown(True)
        self.setItemDelegate(MonitorItemDelegate(self))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self._initMenus()
        self.contextActions = QAction('test', self)
        self.addAction(self.contextActions)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self._showMenu)

        self.doubleClicked.connect(self._doubleClicked)

        self.setSortingEnabled(True)

    def _doubleClicked(self, index):
        probeItem = index.sibling(index.row(), 0)
        if probeItem.data(Qt.UserRole + 1) == "Probe":
            probe = probeItem.data(Qt.UserRole + 3)
            display = probeItem.data(Qt.DisplayRole)
            if probe not in self._viewDialogs.keys():
                self._viewDialogs[probe] = LoggerView(self, probe, display)
                self._viewDialogs[probe].show()
            else:
                self._viewDialogs[probe].show()
                


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

        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localMenu    = QMenu(self.tr('Local Actions'), self)
        self.localMenu.setDisabled(True)
        #######################################################################

        self.configureAction = QAction(self.tr('Configure new action'), self)
        self.configureAction.triggered.connect(monapi.launchUserActionsUI)
        self.targetMenu.addMenu(self.localMenu)
        self.targetMenu.addAction(self.configureAction)




        self.targetMenu.addSeparator()

        targetAction = QAction(self.tr('Suspend all target probes'), self)
        self.targetMenu.addAction(targetAction)

        targetAction = QAction(self.tr('Add entry to the target diary'), self)
        self.targetMenu.addAction(targetAction)

        targetAction = QAction(self.tr('Create a new probe'), self)
        targetAction.triggered[bool].connect(self.createProbe)
        self.targetMenu.addAction(targetAction)

        self.targetMenu.addSeparator()

        targetAction = QAction(self.tr('Delete this target ans his probes'), self)
        self.targetMenu.addAction(targetAction)

        self.targetMenu.addSeparator()

        targetAction = QAction(self.tr('Properties'), self)
        self.targetMenu.addAction(targetAction)

        self.probeMenu  = QMenu(self)

        self.probeMenu.addSeparator()

        probeAction = QAction(self.tr('Add to working view'), self)
        probeAction.triggered[bool].connect(self.addToWorkingView)
        self.probeMenu.addAction(probeAction)

        probeAction = QAction(self.tr('Suspend probe'), self)
        self.probeMenu.addAction(probeAction)

        probeAction = QAction(self.tr('Add entry to the probe diary'), self)
        self.probeMenu.addAction(probeAction)

        probeAction = QAction(self.tr('Force check'), self)
        self.probeMenu.addAction(probeAction)

        self.probeMenu.addSeparator()

        probeAction = QAction(self.tr('Delete this probe'), self)
        self.probeMenu.addAction(probeAction)

        self.probeMenu.addSeparator()

        probeAction = QAction(self.tr('Properties'), self)
        self.probeMenu.addAction(probeAction)


        self.noneMenu = QMenu(self)

        noneAction = QAction(self.tr('Create a new target'), self)
        self.noneMenu.addAction(noneAction)
        noneAction.triggered[bool].connect(self.createTarget)

        noneAction = QAction(self.tr('Select all'), self)
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

    def getSelectedElements(self):
        proxyIndexes = self.selectedIndexes()
        selectionList = list()
        for i in range(len(proxyIndexes)):
            modelIndex = self.proxy.mapToSource(proxyIndexes[i])
            modelItem  = self.model.itemFromIndex(modelIndex)
            selectionList.append(modelItem.name)
        return selectionList

    def userActivity(self, index):
        print "clicked!", self.selectedIndexes()

    def filterThis(self, text):
        self.proxy.setFilterFixedString(text)

    def selectionChanged(self, selected, deselected):
        QTreeView.selectionChanged(self, selected, deselected)

    def _showMenu(self, point):
        index = self.proxy.mapToSource(self.indexAt(point))
        item  = self.model.itemFromIndex(index)
        if      item.__class__.__name__ == 'ProbeItem':
            self.probeMenu.popup(self.mapToGlobal(point))
        elif    item.__class__.__name__ == 'TargetItem':
            self._prepareMenuForTarget(item.name)
            self.targetMenu.popup(self.mapToGlobal(point))
        elif    item.__class__.__name__ == 'NoneType':
            self.noneMenu.popup(self.mapToGlobal(point))

    def _prepareMenuForTarget(self, target):
        uactions = monapi.getUActionsFor(target)
        if len(uactions) == 0:
            self.localMenu.setDisabled(True)
        else:
            self.localMenu.setDisabled(False)
            self.localMenu.clear()
            for i in range(len(uactions)):
                qa = QAction(uactions[i], self)
                callback = partial(self._userAction, target, uactions[i])
                qa.triggered.connect(callback)
                self.localMenu.addAction(qa)

    def _userAction(self, target, action):
        print "tt for %s %s" % (target, action)

    #def mousePressEvent(self, pressEvent):
        #button = pressEvent.button()
        #if button == Qt.MouseButton.RightButton: 
            #QTreeView.mousePressEvent(self, pressEvent)
        #else:
            #QTreeView.mousePressEvent(self, pressEvent) 


class MonitorItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(MonitorItemDelegate, self).__init__(parent)
        self._rrdToolLogo   = QImage(nocapi.nGetImage('rrdtool-logo'))
        self._rrdToolSize   = QSize(80,25)

    def paint(self, painter, option, index):
        if index.data(Qt.UserRole + 1) == None:
            itemRoot = index.sibling(index.row(), 0)
            if itemRoot.data(Qt.UserRole + 1) == "Probe":
                if index.column() == 1:
                    if itemRoot.data(Qt.UserRole + 2) == True:
                        option.rect.setSize(self._rrdToolSize)
                        painter.drawImage(option.rect, self._rrdToolLogo)
                        return
                if index.column() == 2:
                    opts = QStyleOptionProgressBar()
                    opts.rect = option.rect
                    opts.minimum = 0
                    opts.maximum = 100
                    opts.progress = 50
                    QApplication.style().drawControl(QStyle.CE_ProgressBar, opts, painter) 
                    return
        QStyledItemDelegate.paint(self, painter, option, index)
