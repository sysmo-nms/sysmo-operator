from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    MonitorProxyEvents   import ChannelHandler
import    MonitorDashboardArea
from    NewTargetForm   import  AddTargetWizard
from    CommonWidgets   import  *
import  TkorderIcons



##############################################################################
### DASHBOARD TREEVIEW #######################################################
##############################################################################
class DashboardTreeView(QTreeView):
    def __init__(self, parent):
        super(DashboardTreeView, self).__init__(parent)
        DashboardTreeView.singleton = self
        self.model   = DashboardTreeModel(self)
        self.setModel(self.model)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setIconSize(QSize(25, 25)) 
        self.setAnimated(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setObjectName('dashTree')
        self.setStyleSheet('QFrame#dashTree {   \
            background-image: url(./icons/hover_info_files.png); \
            background-repeat: no-repeat;                            \
            background-attachment: fixed;                            \
            background-position: bottom right}')

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

    def userActivity(self, index):
        print "clicked!", self.selectedIndexes()

class DashboardTreeModel(QStandardItemModel):
    def __init__(self, parent):
        super(DashboardTreeModel, self).__init__(parent)
        DashboardTreeModel.singleton = self
        self.setHorizontalHeaderLabels(["Dashboards/Cibles/Sondes"])
        #sigDict = ChannelHandler.singleton.masterSignalsDict
        #sigDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self.setDashboardConf()

    def setDashboardConf(self):
        config1 = dict()
        config1['name']     = 'Vue reseau'
        config1['probes']   = [
            {'secondTestHost-3': ['check_icmp-3-1']},
            {'secondTestHost-2': ['check_icmp-2-1']},
            {'secondTestHost-1': ['check_icmp-1-1']}
        ]

        config2 = dict()
        config2['name']     = 'Vue snmp'
        config2['probes']   = [
            {'secondTestHost-3': ['snmp-walk-properties-3-3', 'snmp-walk-numerics-3-4']},
            {'secondTestHost-2': ['snmp-walk-numerics-2-4']}
        ]
        self._initializeConfig([config1, config2])

    def _initializeConfig(self, configList):
        for config in configList:
            self._createRootNode(config)

    def _createRootNode(self, name):
        self.appendRow(DashboardItem(name))


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

class DashboardItem(QStandardItem):
    def __init__(self, config):
        super(DashboardItem, self).__init__()
        self.name       = config['name']
        self.nodeType   = 'dashboard'
        self.status     = 'UNKNOWN'

        probesDict = ChannelHandler.singleton.probes
        targetDict = dict()
        print probesDict
        #for probe in config['probes']:
            

        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.name
        else:
            return QStandardItem.data(self, role)

    def _getIconStatus(self):
        if self.status  == 'UNKNOWN':
            return TkorderIcons.get('weather-clear-night')
        elif self.status == 'WARNING':
            return TkorderIcons.get('weather-showers')
        elif self.status == 'CRITICAL':
            return TkorderIcons.get('weather-severe-alert')
        elif self.status == 'OK':
            return TkorderIcons.get('weather-clear')

class TargetItem(QStandardItem):
    def __init__(self, data):
        super(TargetItem, self).__init__()
        self.name       = data['value']['name']
        self.nodeType   = 'target'
        self.status     = 'UNKNOWN'
        self.searchString   = self.name
        self.targetDict = data
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
