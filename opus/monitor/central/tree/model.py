from    PySide.QtCore   import (
    Qt,
    QTimer
)
from    PySide.QtGui    import (
    QStandardItemModel,
    QStandardItem
)

import nocapi
import opus.monitor.api as monapi

class ProbeModel(QStandardItemModel):
    def __init__(self, parent):
        super(ProbeModel, self).__init__(parent)
        ProbeModel.singleton = self
        self._probeView = parent
        self._probeItems  = dict()
        self._targetItems = dict()
        self.ticsignal = QTimer()
        self.ticsignal.setInterval(1000)
        self.ticsignal.setSingleShot(False)
        self.ticsignal.start()

        self.setHorizontalHeaderLabels([
                "Targets/Probes",
                "Loggers",
                "Progress",
                "Status",
                "Step/Timeout",
                "State",
                "Ip|Host",
                "Command"
        ])
        monapi.connectToEvent('targetInfo', self._handleTargetInfo)
        monapi.connectToEvent('probeInfo',  self._handleProbeInfo)
        monapi.connectToEvent('probeActivity', self._handleProbeActivity)

    def _handleProbeActivity(self, msg):
        target = msg['value']['target']
        (boo,parent) = self._itemExist(target)
        if boo == False: return
        parent.handleProbeActivity(msg)

    def _handleTargetInfo(self, msg):
        (boo, target) = self._itemExist(msg['value']['name'])
        if boo == False:
            self.appendRow(TargetItem(msg))
        else:
            self._updateRow(target, msg)

    def _handleProbeInfo(self, msg):
        target = msg['value']['target']
        (_, parent) = self._itemExist(target)
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
        self.probeSearchStrings = list()
        self.targetDict = data
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.setColumnCount(8)
        self._generateToolTip()

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            if self.targetDict['value']['properties']['sysName'] != "undefined":
                return self.targetDict['value']['properties']['sysName']
            elif self.targetDict['value']['properties']['dnsName'] != "undefined":
                return self.targetDict['value']['properties']['dnsName']
            elif self.targetDict['value']['properties']['staticName'] != "undefined":
                return self.targetDict['value']['properties']['staticName']
            else:
                return self.targetDict['value']['name']
        elif role == Qt.UserRole:
            searchString = ""
            for i in range(self.rowCount()):
                searchString += self.child(i).descr
            return self.data(Qt.DisplayRole) + searchString
        elif role == (Qt.UserRole + 1):
            return "Target"
        elif role == (Qt.UserRole + 2):
            return self.targetDict['value']['properties']['ip']
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
            self.appendRow(ProbeItem(msg, self))
        else:
            child.updateState(msg)

        self._setWorstStatus()
        self.emitDataChanged()

    def handleProbeActivity(self, msg):
        count = self.rowCount()
        probe = msg['value']['name']
        for i in range(count):
            if self.child(i).name == probe:
                self.child(i).handleActivity(msg)
                break

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
    def __init__(self, data, parentItem):
        super(ProbeItem, self).__init__()
        self._ticvalue = 0
        ProbeModel.singleton.ticsignal.timeout.connect(self._tictimeout)
        if 'bmonitor_logger_rrd' in data['value']['loggers'].keys():
            self._logsRrd = True
        else:
            self._logsRrd = False

        self._parentItem = parentItem
        self._lastReturn = ""
        self._type      = data['value']['probeMod']
        self.name       = data['value']['name']
        self.descr      = data['value']['descr']
        self.nodeType   = 'probe'
        self.target     = data['value']['target']
        self.status     = data['value']['status']
        self.probeDict = data
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.setColumnCount(8)


    def handleActivity(self, msg):
        self._ticvalue = 0
        self._lastReturn = msg['value']['textual']
        self.emitDataChanged()

    def _tictimeout(self):
        #print "tictimeout: ", self.descr
        self._ticvalue = self._ticvalue + 1
        self.emitDataChanged()

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._getIconStatus()
        elif role == Qt.DisplayRole:
            return self.probeDict['value']['descr']
        elif role == Qt.UserRole:
            target = self._parentItem.data(Qt.DisplayRole)
            probe  = self.probeDict['value']['descr']
            return target + probe
        elif role == (Qt.UserRole + 1):
            return "Probe"
        elif role == (Qt.UserRole + 2):
            return self._logsRrd
        elif role == (Qt.UserRole + 3):
            return self.name
        elif role == (Qt.UserRole + 4):
            return self._ticvalue
        elif role == (Qt.UserRole + 5):
            return self.probeDict['value']['step']
        elif role == (Qt.UserRole + 6):
            return self.probeDict['value']['timeout']
        elif role == (Qt.UserRole + 7):
            return self.probeDict['value']['active']
        elif role == (Qt.UserRole + 8):
            if self._type == 'bmonitor_probe_ncheck':
                return self.probeDict['value']['probeconf']
            else:
                return ''
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
