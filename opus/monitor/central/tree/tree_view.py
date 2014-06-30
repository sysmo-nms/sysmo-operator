from    PySide.QtCore   import (
    Qt,
    QSize,
    QSettings
)

from    PySide.QtGui    import (
    QTreeView,
    QSortFilterProxyModel,
    QMenu,
    QAction,
    QAbstractItemView
)

from    functools import partial
from    opus.monitor.commands.wizards           import UserActionsWizard
from    opus.monitor.central.tree.logwin        import openLoggerFor
from    opus.monitor.central.tree.tree_model    import ProbeModel
from    opus.monitor.central.tree.menus.probe   import ProbeMenu
from    opus.monitor.central.tree.menus.target  import TargetMenu
import  opus.monitor.central.tree.tree_delegate as pdelegate
import  opus.monitor.api                        as monapi
import  nocapi

class ProbesTreeview(QTreeView):
    def __init__(self, parent):
        super(ProbesTreeview, self).__init__(parent)
        nocapi.nConnectWillClose(self._saveSettings)
        ProbesTreeview.singleton = self
        self._viewDialogs = dict()
        
        # QTreeView conf
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setDropIndicatorShown(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showMenu)
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
        self.setSortingEnabled(True)
        self.doubleClicked.connect(self._doubleClicked)


        # model conf
        self.model   = ProbeModel(self)
        self.proxy   = QSortFilterProxyModel(self)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setDynamicSortFilter(True)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterRole(Qt.UserRole)
        self.setModel(self.proxy)


        # delegates
        self.setItemDelegateForColumn(1, pdelegate.LoggerItemDelegate(self))
        self.setItemDelegateForColumn(2, pdelegate.ProgressItemDelegate(self))
        self.setItemDelegateForColumn(3, pdelegate.StatusItemDelegate(self))
        self.setItemDelegateForColumn(4, pdelegate.TriggerItemDelegate(self))
        self.setItemDelegateForColumn(5, pdelegate.StateItemDelegate(self))
        self.setItemDelegateForColumn(6, pdelegate.HostItemDelegate(self))
        self.setItemDelegateForColumn(7, pdelegate.TimelineItemDelegate(self))

        # setings
        settings = QSettings()
        state   = settings.value('monitor/probe_treeview_header')
        if state != None:
            header = self.header()
            header.restoreState(state)

        # various init
        self.targetMenu = TargetMenu(self)
        self.probeMenu  = ProbeMenu(self)
        #self._initMenus()

    def _saveSettings(self):
        header = self.header()
        settings = QSettings()
        settings.setValue('monitor/probe_treeview_header', header.saveState())

    def _doubleClicked(self, index):
        probeItem = index.sibling(index.row(), 0)
        if probeItem.data(Qt.UserRole + 1) == "Probe":
            probe = probeItem.data(Qt.UserRole + 3)
            display = probeItem.data(Qt.DisplayRole)
            openLoggerFor(probe, display)

    def filterThis(self, text):
        self.proxy.setFilterFixedString(text)
                
    def getSelectedElements(self):
        proxyIndexes = self.selectedIndexes()
        selectionList = list()
        for i in range(len(proxyIndexes)):
            modelIndex = self.proxy.mapToSource(proxyIndexes[i])
            modelItem  = self.model.itemFromIndex(modelIndex)
            selectionList.append(modelItem.name)
        return selectionList

    def _showMenu(self, point):
        index = self.proxy.mapToSource(self.indexAt(point))
        item  = self.model.itemFromIndex(index)
        if      item.__class__.__name__ == 'ProbeItem':
            self.probeMenu.showMenuFor(item.name, point)
        elif    item.__class__.__name__ == 'TargetItem':
            self.targetMenu.showMenuFor(item.name, point)
        elif    item.__class__.__name__ == 'NoneType': pass
