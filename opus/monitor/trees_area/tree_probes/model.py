from    PySide.QtCore   import Qt
from    PySide.QtGui    import (
    QStandardItemModel,
    QStandardItem
)

import nocapi
import opus.monitor.api as monapi

class ProbeModel(QStandardItemModel):
    def __init__(self, parent):
        super(ProbeModel, self).__init__(parent)
        self.setHorizontalHeaderLabels([
                "Targets/Probes",
                "Loggers",
                "Next return",
                "Status",
                "Description",
                "Step/Timeout",
                "State",
                "Ip address",
                "Last return"
        ])
        self.setColumnCount(9)
        monapi.connectToEvent('targetInfo', self._handleTargetInfo)
        monapi.connectToEvent('probeInfo',  self._handleProbeInfo)

    def _handleTargetInfo(self, msg):
        (boo, target) = self._itemExist(msg['value']['name'])
        print "add target: ", msg['value']['name']
        if boo == False:
            self.appendRow(TargetItem(msg))
        else:
            self._updateRow(target, msg)

    def _handleProbeInfo(self, msg):
        target = msg['value']['target']
        (boo, parent) = self._itemExist(target)
        if boo == False:
            print "parent did not exist:", target
            self.appendRow(ProbeItem(msg))
        else:
            print "parent exist:", target
            parent.handleProbeInfo(msg)

    def _updateRow(self, item, msg):
        item.updateState(msg)

    def _itemExist(self, itemName):
        rootItem = self.invisibleRootItem()
        for row in range(rootItem.rowCount()):
            child = rootItem.child(row)
            if child.name == itemName:
                return (True, child)
        return (False, None)

    def supportedDropActions(self):
        return Qt.MoveAction

class TargetItem(QStandardItem):
    def __init__(self, data):
        super(TargetItem, self).__init__()
        self.name       = data['value']['name']
        self.nodeType   = 'target'
        self.status     = 'UNKNOWN'
        self.searchString   = self.name
        self.targetDict = data
        self.setFlags(Qt.ItemIsEnabled)
        self.setColumnCount(9)
        self._generateToolTip()

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.targetDict['value']['properties']['sysName']
        elif role == Qt.UserRole:
            return self.searchString
        elif role == (Qt.UserRole + 1):
            return "Target"
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
        self._generateToolTip()

    def _generateToolTip(self):
        props   = self.targetDict['value']['properties']
        table = "<table>"
        for k in props.keys():
            row = "<tr><td><b>%s</b></td><td>: %s</td></tr>" % (k, props[k])
            table = table + row
        table = table + "</table>"
        self.setToolTip(table)

    def __lt__(self, other): pass

    def _getIconStatus(self):
        if self.status  == 'UNKNOWN':
            return nocapi.nGetIcon('weather-clear-night')
        elif self.status == 'WARNING':
            return nocapi.nGetIcon('weather-showers')
        elif self.status == 'CRITICAL':
            return nocapi.nGetIcon('weather-severe-alert')
        elif self.status == 'OK':
            return nocapi.nGetIcon('weather-clear')

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
        if 'bmonitor_logger_rrd' in data['value']['loggers'].keys():
            self._logsRrd = True
        else:
            self._logsRrd = False

        self.name       = data['value']['name']
        self.nodeType   = 'probe'
        self.target     = data['value']['target']
        self.status     = data['value']['status']
        self.searchString = self.name + self.target
        self.probeDict = data
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsDragEnabled)
        self.setColumnCount(9)


    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.probeDict['value']['descr']
        elif role == Qt.UserRole:
            return self.searchString
        elif role == (Qt.UserRole + 1):
            return "Probe"
        elif role == (Qt.UserRole + 2):
            return self._logsRrd
        elif role == (Qt.UserRole + 3):
            return self.name
        else:
            return QStandardItem.data(self, role)

    def updateState(self, data):
        self.status     = data['value']['status']
        self.probeDict  = data
        self.emitDataChanged()

    def __lt__(self, other): pass

    def _getIconStatus(self):
        if self.status == 'UNKNOWN':
            return nocapi.nGetIcon('weather-clear-night')
        if self.status == 'WARNING':
            return nocapi.nGetIcon('weather-showers')
        if self.status == 'CRITICAL':
            return nocapi.nGetIcon('weather-severe-alert')
        if self.status == 'OK':
            return nocapi.nGetIcon('weather-clear')
