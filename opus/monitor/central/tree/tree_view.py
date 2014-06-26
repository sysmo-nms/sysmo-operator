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
from    opus.monitor.central.tree.logwin        import LoggerView
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
            if probe not in self._viewDialogs.keys():
                self._viewDialogs[probe] = LoggerView(self, probe, display)
                self._viewDialogs[probe].show()
            else:
                self._viewDialogs[probe].show()

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


class TargetMenu(QMenu):
    def __init__(self, parent):
        super(TargetMenu, self).__init__(parent)
        self._tuActionWiz  = None
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localMenu    = QMenu(self.tr('Local Actions'), self)
        self.localMenu.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self.localMenu.setDisabled(True)

        self.configureAction = QAction(self.tr('Configure new action'), self)
        self.addMenu(self.localMenu)
        self.addAction(self.configureAction)
        #######################################################################

        self.addSeparator()

        action = QAction(self.tr('Suspend all target probes'), self)
        action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)

        action = QAction(self.tr('Add entry to the target diary'), self)
        self.addAction(action)


        action = QAction(self.tr('Create a new probe'), self)
        action.setIcon(nocapi.nGetIcon('list-add'))
        action.triggered[bool].connect(self._createProbeAction)
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Delete this target ans his probes'), self)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()


        action = QAction(self.tr('Documentation'), self)
        action.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self.addAction(action)

        action = QAction(self.tr('History'), self)
        self.addAction(action)

        action = QAction(self.tr('Performances'), self)
        self.addAction(action)

        action = QAction(self.tr('Properties'), self)
        self.addAction(action)

    def showMenuFor(self, target, point):
        uactions = monapi.getUActionsFor(target)
        if self._tuActionWiz != None:
            self.configureAction.triggered.disconnect(self._tuActionWiz)
        self._tuActionWiz = partial(self._launchUserActionsWiz, target)
        self.configureAction.triggered.connect(self._tuActionWiz)
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

        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _createProbeAction(self, msg):
        print "create prboe ", msg

    def _userAction(self, element, action):
        monapi.execUAction(action, element)


class ProbeMenu(QMenu):
    def __init__(self, parent):
        super(ProbeMenu, self).__init__(parent)
        self._puActionWiz  = None
        #######################################################################
        ## DYNAMIC TARGETS MENUS ##############################################
        #######################################################################
        self.localProbeMenu    = QMenu(self.tr('Local Actions'), self)
        self.localProbeMenu.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self.localProbeMenu.setDisabled(True)

        self.configureProbeAction = QAction(self.tr('Configure new action'), self)
        self.addMenu(self.localProbeMenu)
        self.addAction(self.configureProbeAction)
        #######################################################################

        self.addSeparator()

        action = QAction(self.tr('Open log viewew'), self)
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Open probe documentation'), self)
        action.setIcon(nocapi.nGetIcon('folder-saved-search'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Suspend probe'), self)
        action.setIcon(nocapi.nGetIcon('media-playback-pause'))
        self.addAction(action)

        action = QAction(self.tr('Add entry to the probe diary'), self)
        self.addAction(action)

        action = QAction(self.tr('Force check'), self)
        action.setIcon(nocapi.nGetIcon('software-update-available'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Delete this probe'), self)
        action.setIcon(nocapi.nGetIcon('process-stop'))
        self.addAction(action)

        self.addSeparator()

        action = QAction(self.tr('Properties'), self)
        self.addAction(action)

    def showMenuFor(self, probe, point):
        uactions = monapi.getUActionsFor(probe)
        if self._puActionWiz != None:
            self.configureProbeAction.triggered.disconnect(self._puActionWiz)
        self._puActionWiz = partial(self._launchUserActionsWiz, probe)
        self.configureProbeAction.triggered.connect(self._puActionWiz)
        if len(uactions) == 0:
            self.localProbeMenu.setDisabled(True)
        else:
            self.localProbeMenu.setDisabled(False)
            self.localProbeMenu.clear()
            for i in range(len(uactions)):
                qa = QAction(uactions[i], self)
                callback = partial(self._userAction, probe, uactions[i])
                qa.triggered.connect(callback)
                self.localProbeMenu.addAction(qa)

        point.setX(point.x() + 12)
        self.popup(self.parent().mapToGlobal(point))

    def _launchUserActionsWiz(self, elem):
        uaWiz = UserActionsWizard(self, element=elem)

    def _userAction(self, element, action):
        monapi.execUAction(action, element)
