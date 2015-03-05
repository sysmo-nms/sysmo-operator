from    PyQt5.QtCore   import (
    Qt,
    QSize,
    QSortFilterProxyModel,
    QSettings
)

from    PyQt5.QtWidgets    import (
    QTreeView,
    QMenu,
    QAction,
    QAbstractItemView
)

from    functools import partial
from    monitor.commands.wizards           import UserActionsWizard
from    monitor.elements_properties.probe.main import openPropertiesFor
from    monitor.gui.tree.tree_model    import ProbeModel
from    monitor.context_menus.probe   import ProbeMenu
from    monitor.context_menus.target  import TargetMenu
import  monitor.commands.user_actions
import  monitor.gui.tree.tree_delegate as pdelegate
import  monitor.api                        as monapi
import  sysmapi

class ProbesTreeview(QTreeView):
    def __init__(self, parent):
        super(ProbesTreeview, self).__init__(parent)
        sysmapi.nConnectWillClose(self._saveSettings)
        ProbesTreeview.singleton = self
        self._viewDialogs = dict()
        
        # QTreeView conf
        self.setItemsExpandable(False)
        self.setRootIsDecorated(False)
        self.setWordWrap(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showMenu)
        self.setObjectName('backTree')
        self.setIconSize(QSize(20, 20)) 
        self.setAnimated(False)
        self.setAlternatingRowColors(True)
        self.setStyleSheet('''QFrame#backTree { 
            background-image: url(./graphics/hover_info_files.png);
            background-repeat: no-repeat;
            background-color: %s;
            background-attachment: fixed; 
            background-position: bottom right}''' % sysmapi.nGetRgb('Base'))
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
        #self.setItemDelegateForColumn(1, pdelegate.LoggerItemDelegate(self))
        self.setItemDelegateForColumn(1, pdelegate.ProgressItemDelegate(self))
        #self.setItemDelegateForColumn(2, pdelegate.StatusItemDelegate(self))
        #self.setItemDelegateForColumn(3, pdelegate.TriggerItemDelegate(self))
        #self.setItemDelegateForColumn(4, pdelegate.StateItemDelegate(self))
        #self.setItemDelegateForColumn(5, pdelegate.HostItemDelegate(self))
        #self.setItemDelegateForColumn(7, pdelegate.TimelineItemDelegate(self))

        # setings
        settings = QSettings()
        state   = settings.value('monitor/probe_treeview_header')
        if state is not None:
            header = self.header()
            header.restoreState(state)

        # various init
        self.targetMenu = TargetMenu(self)
        self.probeMenu  = ProbeMenu(self)

    def _saveSettings(self):
        header = self.header()
        settings = QSettings()
        settings.setValue('monitor/probe_treeview_header', header.saveState())

    def _doubleClicked(self, index):
        item = index.sibling(index.row(), 0)
        if item.data(Qt.UserRole + 1) == "Probe":
            print(item)
            probe   = item.data(Qt.UserRole + 3)
            display = item.data(Qt.DisplayRole)
            openPropertiesFor(probe, display)
        else:
            targetid = item.data(Qt.UserRole + 1)
            monitor.commands.user_actions.launchOperationFor(self, targetid)

    def filterThis(self, text):
        self.proxy.setFilterFixedString(text)
        self.expandAll()
                
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
