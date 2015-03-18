from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import sysmapi
import monitor.api as monapi

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
                "Progress",
                "Status",
                "Step/Timeout",
                "State",
                "Host",
                "Last 72 hours timeline"
        ])
        monapi.connectToEvent('infoTarget', self._handleTargetInfo)
        monapi.connectToEvent('infoProbe',  self._handleProbeInfo)
        monapi.connectToEvent('deleteTarget', self._handleTargetDelete)
        monapi.connectToEvent('deleteProbe', self._handleProbeDelete)

        monapi.connectToEvent('probeReturn', self._handleProbeReturn)

    def _handleProbeReturn(self, msg):
        target = msg['value']['target']
        (boo,parent) = self._itemExist(target)
        if boo == False: return
        parent.handleProbeReturn(msg)
        self._probeView.expandAll()

    def _handleTargetDelete(self, msg):
        elem = msg['value']['name']
        (boo,target) = self._itemExist(elem)
        if boo == False: return
        self.removeRow(target.row())
        self._probeView.expandAll()

    def _handleProbeDelete(self, msg):
        elem = msg['value']['target']
        (boo,target) = self._itemExist(elem)
        if boo == False: return
        target.handleProbeDelete(msg)
        self._probeView.expandAll()


    def _handleTargetInfo(self, msg):
        (boo, target) = self._itemExist(msg['value']['name'])
        if boo == False:
            t = TargetItem(msg)
            self.appendRow([
                t, t.row2, t.row3_status,
                t.row4, t.row5, t.row6_host, t.row7_timeline])
                #t.row4, t.row5, t.row6_host, t.row7_timeline])
        else:
            self._updateRow(target, msg)
        self._probeView.expandAll()

    def _handleProbeInfo(self, msg):
        target = msg['value']['target']
        (_, parent) = self._itemExist(target)
        parent.handleProbeInfo(msg)
        self._probeView.expandAll()

    def _updateRow(self, item, msg):
        item.updateState(msg)
        self._probeView.expandAll()

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
        self.status     = 'DOWN'
        self.probeSearchStrings = list()
        self.targetDict = data
        self.nodeIconType = data['value']['properties']['type']
        self.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.setColumnCount(8)
        self._initIcon()
        self._initColumnItems()
        self._generateToolTip()

    def _initIcon(self):
        if self.nodeIconType == 'server':
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('server'))
        elif self.nodeIconType == 'router':
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('router'))
        elif self.nodeIconType == 'switch':
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('switch'))
        elif self.nodeIconType == 'wireless':
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('wireless'))
        elif self.nodeIconType == 'firewall':
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('firewall'))
        elif self.nodeIconType == 'printer':
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('printer'))
        else:
            self.nodeIcon = QIcon(sysmapi.nGetPixmap('computer'))

    def _initColumnItems(self):
        #self.row1       = QStandardItem()
        self.row2       = QStandardItem()
        self.row4       = QStandardItem()
        self.row5       = QStandardItem()

        self.row3_status    = QStandardItem()
        self.row6_host      = QStandardItem()
        self.row7_timeline  = QStandardItem()

        #self.row3_status.setData('status', role=Qt.DisplayRole)
        self.row6_host.setData(self.targetDict['value']['properties']['host'], role=Qt.DisplayRole)
        self.row7_timeline.setData('', role=Qt.DisplayRole)

    def data(self, role):
        name = self.targetDict['value']['properties']['name']
        if   role == Qt.DecorationRole:
            return self.nodeIcon
        elif role == Qt.DisplayRole:
            if self.targetDict['value']['properties']['sysName'] != "undefined":
                return self.targetDict['value']['properties']['sysName']
            elif name != "undefined" and name != "":
                return self.targetDict['value']['properties']['name']
            else:
                return self.targetDict['value']['properties']['host']
        elif role == Qt.UserRole:
            searchString = ""
            for i in range(self.rowCount()):
                searchString += self.child(i).descr
            return self.data(Qt.DisplayRole) + searchString
        elif role == (Qt.UserRole + 1):
            return self.targetDict['value']['properties']['staticName']
        #elif role == (Qt.UserRole + 2):
            #return self.targetDict['value']['properties']['host']
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
            p = ProbeItem(msg, self)
            self.appendRow([
                p, p.row2_progress, p.row3_status, 
                p.row4_trigger, p.row5_state, p.row6_host, p.row7_timeline])
                #p.row4_trigger, p.row5_state, p.row6_host, p.row7_time])
        else:
            child.updateState(msg)

        self._setWorstStatus()
        self.emitDataChanged()

    def handleProbeDelete(self, msg):
        count = self.rowCount()
        probe = msg['value']['name']
        for i in range(count):
            if self.child(i) is not None:
                if self.child(i).name == probe:
                    self.removeRow(i)

    def handleProbeReturn(self, msg):
        count = self.rowCount()
        probe = msg['value']['name']
        for i in range(count):
            if self.child(i).name == probe:
                self.child(i).handleReturn(msg)
                break
        self.emitDataChanged()

    def updateState(self, msg):
        self.targetDict = msg
        self._generateToolTip()

    def _generateToolTip(self):
        props   = self.targetDict['value']['properties']
        table = "<table>"
        for k in list(props.keys()):
            row = "<tr><td><b>%s</b></td><td>: %s</td></tr>" % (k, props[k])
            table = table + row
        table = table + "</table>"
        self.setToolTip(table)

    def __lt__(self, other): pass

    def _setWorstStatus(self): pass
    def _setWorstStatus2(self):
        count = self.rowCount()
        status = list()
        for i in range(count):
            probe = self.child(i)
            status.append(probe.status)

        if 'DOWN' in status:
            self.row3_status.setIcon(QIcon(sysmapi.nGetPixmap('weather-clear-night')))
        elif 'CRITICAL' in status:
            self.row3_status.setIcon(QIcon(sysmapi.nGetPixmap('weather-severe-alert')))
        elif 'WARNING' in status:
            self.row3_status.setIcon(QIcon(sysmapi.nGetPixmap('weather-showers')))
        elif 'OK' in status:
            self.row3_status.setIcon(QIcon(sysmapi.nGetPixmap('weather-clear')))
        else:
            self.row3_status.setIcon(QIcon())


class ProgressItem(QStandardItem):
    TimeoutRole     = Qt.UserRole + 1
    StepRole        = Qt.UserRole + 2
    ProgressRole    = Qt.UserRole + 3
    def __init__(self, data):
        super(ProgressItem, self).__init__()
        step, timeout   = data
        self._progress  = 0
        self._step      = step
        self._timeout   = timeout
        self.setToolTip('Time to wait before a new check')
        ProbeModel.singleton.ticsignal.timeout.connect(self._tictimeout)
        self._initData()

    def setRemaining(self, millisec):
        self._progress = self._step - int(millisec / 1000)
        self._updateData()

    def _initData(self):
        display = '%s/%s' % (self._progress, self._step)
        self.setData(display, role=Qt.DisplayRole)
        self.setData(self._step,     ProgressItem.StepRole)
        self.setData(self._timeout,  ProgressItem.TimeoutRole)
        self.setData(self._progress, ProgressItem.ProgressRole)

    def _updateData(self):
        display = '%s/%s' % (self._progress, self._step)
        self.setData(display, role=Qt.DisplayRole)
        self.setData(self._progress, ProgressItem.ProgressRole)

    def _tictimeout(self):
        self._progress = self._progress + 1
        self._updateData()

    def reset(self):
        self._progress = 0
        self._updateData()

class LoggerItem(QStandardItem):
    LoggersRole = Qt.UserRole + 1
    def __init__(self, loggers):
        super(LoggerItem, self).__init__()
        self.setData(loggers, LoggerItem.LoggersRole)
        display = ''
        for i in range(len(loggers)):
            display = display + " " + loggers[i] 
        self.setData(display, Qt.DisplayRole)

class ProbeItem(QStandardItem):
    def __init__(self, data, parentItem):
        super(ProbeItem, self).__init__()
        self._ticvalue = 0
        #ProbeModel.singleton.ticsignal.timeout.connect(self._tictimeout)


        self._decoIcon = QIcon(sysmapi.nGetPixmap('satellite'))
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
        self._initColumnItems()

    def _initColumnItems(self):
        #loggers = list(self.probeDict['value']['loggers'].keys())
        #self.row1_log   = LoggerItem(loggers)

        timeout = self.probeDict['value']['timeout']
        step    = self.probeDict['value']['step']
        self.row2_progress = ProgressItem((step, timeout))

        self.row3_status = QStandardItem('b')
        self.row3_status.setIcon(QIcon(sysmapi.nGetPixmap('satellite')))
        self.row3_status.setData(self.probeDict['value']['status'], role=Qt.DisplayRole)

        self.row4_trigger = QStandardItem()
        string = '%s/%s' % (self.probeDict['value']['step'], self.probeDict['value']['timeout'])
        self.row4_trigger.setData(string, role=Qt.DisplayRole)

        self.row5_state = QStandardItem()
        if self.probeDict['value']['active']:
            self.row5_state.setIcon(QIcon(sysmapi.nGetPixmap('satellite')))
            self.row5_state.setData('running', role=Qt.DisplayRole)
        else:
            self.row5_state.setIcon(QIcon(sysmapi.nGetPixmap('satellite')))
            self.row5_state.setData('stopped', role=Qt.DisplayRole)

        self.row6_host  = QStandardItem()
        #self.row6_host.setData('host', role=Qt.DisplayRole)

        self.row7_timeline  = QStandardItem()
        self.row7_timeline.setData('timeline', role=Qt.DisplayRole)


    def handleReturn(self, msg):
        self.setToolTip(msg['value']['replyString'])
        val = msg['value']['nextReturn']
        self.row2_progress.setRemaining(val)

    def data(self, role):
        if   role == Qt.DecorationRole:
            return self._decoIcon
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
        self.row3_status.setData(self.status, role=Qt.DisplayRole)
        self.probeDict  = data
        self.emitDataChanged()

    def __lt__(self, other): pass

    def _getIconStatus(self):
        if self.status == 'DOWN':
            return QIcon(sysmapi.nGetPixmap('weather-clear-night'))
        if self.status == 'WARNING':
            return QIcon(sysmapi.nGetPixmap('weather-showers'))
        if self.status == 'CRITICAL':
            return QIcon(sysmapi.nGetPixmap('weather-severe-alert'))
        if self.status == 'OK':
            return QIcon(sysmapi.nGetPixmap('weather-clear'))
