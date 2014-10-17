from    PySide.QtCore   import (
    QObject,
    Signal,
    QTemporaryFile
)
from    collections         import deque
from    noctopus_widgets    import NFrameContainer
import  nocapi
import  re
import  supercast.main              as supercast
import  opus.monitor.norrd          as norrd
import  opus.monitor.http_manager   as httpman
import  xml.etree.ElementTree as ET


class ChanHandler(QObject):
    
    " This class handle other widgets subscription and emit message "
    " received by the server with Signal(). The method 'handleMSG' receive "
    " messages from the server "
    " She is also responsible of the channel group concept and max channel "
    " limitations."

    def __init__(self, parent, maxChans=3):
        super(ChanHandler, self).__init__(parent)
        ChanHandler.singleton = self
        
        nocapi.nConnectSupercastEnabled(self._initSupercast)

        self._initChanHandling()
        self._initSignals()

    def _initSupercast(self):
        nocapi.nSetMessageProcessor('modMonitorPDU', self.handleSupercastMsg)

    def _initChanHandling(self):
        self._masterChan        = 'target-MasterChan'
        self._masterChanRunning = False
        self._subscribedChans   = list()
        self._pendingSubscribe  = list()
        self._chanProxy         = dict()
        self.targets            = dict()
        self.probes             = dict()

    def _initSignals(self):
        # signals
        self.masterSignalsDict = dict()
        self.masterSignalsDict['probeInfo']     = SimpleSignal(self)
        self.masterSignalsDict['targetInfo']    = SimpleSignal(self)
        self.masterSignalsDict['probeModInfo']  = SimpleSignal(self)
        self.masterSignalsDict['probeActivity'] = SimpleSignal(self)
        self.masterSignalsDict['probeDump']     = SimpleSignal(self)
        self.masterSignalsDict['probeReturn']   = SimpleSignal(self)
        self.masterSignalsDict['probeEventMsg'] = SimpleSignal(self)
        self.masterSignalsDict['rrdLoggerEventMsg'] = SimpleSignal(self)

        # connect myself
        self.masterSignalsDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self.masterSignalsDict['targetInfo'].signal.connect(self._handleTargetInfo)
        self.masterSignalsDict['probeDump'].signal.connect(self._handleProbeDump)
        self.masterSignalsDict['probeReturn'].signal.connect(self._handleProbeReturn)
        self.masterSignalsDict['probeEventMsg'].signal.connect(self._handleEventMsg)
        self.masterSignalsDict['rrdLoggerEventMsg'].signal.connect(self._handleRrdLoggerEventMsg)
        # END

    def handleSupercastMsg(self, msg):
        if      msg['msgType'] == 'probeReturn':
            self.masterSignalsDict['probeReturn'].signal.emit(msg)

        elif    msg['msgType'] == 'probeEventMsg':
            self.masterSignalsDict['probeEventMsg'].signal.emit(msg)

        elif    msg['msgType'] == 'rrdLoggerEvent':
            self.masterSignalsDict['rrdLoggerEventMsg'].signal.emit(msg)

        elif    msg['msgType'] == 'probeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'rrdFileDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'rrdProbeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'eventProbeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'probeInfo':
            self.masterSignalsDict['probeInfo'].signal.emit(msg)

        elif    msg['msgType'] == 'targetInfo':
            self.masterSignalsDict['targetInfo'].signal.emit(msg)

        elif    msg['msgType'] == 'probeModInfo':
            self.masterSignalsDict['probeModInfo'].signal.emit(msg)

        elif    msg['msgType'] == 'probeActivity':
            self.masterSignalsDict['probeActivity'].signal.emit(msg)

        elif    msg['msgType'] == 'staticChanInfo':
            chan    = msg['value']
            action  = msg['event']
            if chan == self._masterChan and action == 'create':
                self._autoSubscribe()

        elif    msg['msgType'] == 'subscribeOk':
            self._handleSubscribeOk(msg)

        elif    msg['msgType'] == 'unSubscribeOk':
            self._handleUnsubscribeOk(msg)
        else: 
            print "unknown msg received", msg['msgType']

    def subscribe(self, viewObject, channel):
        if channel in self._subscribedChans:
            self._chanProxy[channel].synchronizeView(viewObject)
            self._chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
        elif channel in self._pendingSubscribe:
            self._chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
        else:
            self._chanProxy[channel] = Channel(self, channel)
            self._chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
            self._subscribe(channel)

    def unsubscribe(self, viewObject, channel):
        self._chanProxy[channel].signal.disconnect(viewObject.handleProbeEvent)

    def _subscribe(self, channel):
        self._pendingSubscribe.append(channel)
        nocapi.nSubscribe(self.handleSupercastMsg, channel)

    def _unsubscribe(self, channel):
        self.pendingUnsubscribe.append(channel)
        nocapi.nUnsubscribe(self.handleSupercastMsg, channel)

    def _handleSubscribeOk(self, msg):
        channel = msg['value']
        if channel == self._masterChan: pass
        self._pendingSubscribe.remove(channel)
        self._subscribedChans.append(channel)


    def _handleUnsubscribeOk(self, msg):
        channel = msg['value']
        if channel == self._masterChan: return
        self.chanSignals[channel].destroy()
        del self.chanSignals[channel]

    def _handleProbeDump(self, msg):
        channel = msg['value']['id']
        self._chanProxy[channel].handleDump(msg)

    def _handleProbeReturn(self, msg):
        channel = msg['value']['id']
        self._chanProxy[channel].handleReturn(msg)

    def _handleRrdLoggerEventMsg(self, msg):
        channel = msg['value']['id']
        self._chanProxy[channel].handleRrdLoggerEvent(msg)

    def _handleEventMsg(self, msg):
        channel = msg['value']['id']
        self._chanProxy[channel].handleEvent(msg)

    def _handleProbeInfo(self, msg):
        probeInfo   = msg['value']
        probeName   = probeInfo['name']
        self.probes[probeName] = probeInfo

    def _handleTargetInfo(self, msg):
        targetInfo  = msg['value']
        targetName  = targetInfo['name']
        self.targets[targetName] = targetInfo

    # startup subscribe
    def _autoSubscribe(self):
        nocapi.nSubscribe(self._handleAutoSubscribe, self._masterChan)

    def _handleAutoSubscribe(self, msg):
        if msg['msgType'] == 'subscribeOk':
            self._masterchanRunning = True
            nocapi.nQuery('getChecksInfo', self._handleChecksInfo)
        else:
            print "error: ", msg

    def _handleChecksInfo(self, msg):
        checkInfos = dict()
        checkDefs = msg['value']['infos']
        for i in range(len(checkDefs)):
            root = ET.fromstring(checkDefs[i])
            chk  = root.attrib['command']
            checkInfos[chk] = dict()
            checkInfos[chk]['path']  = root.find('path').text
            checkInfos[chk]['descr'] = root.find('descr').text

            fdict = dict()
            finfo = root.find('flags_def')
            for i in finfo.findall('flag_info'):
                name = i.attrib['name']
                fdict[name] = dict()
                fdict[name]['usage']   = i.find('usage').text
                fdict[name]['default'] = i.find('default').text
                fdict[name]['role']    = i.find('role').text
            checkInfos[chk]['flags_def'] = fdict
        self.checkInfos = checkInfos

    def getCheckInfos(self):
        return self.checkInfos

class Channel(QObject):
    signal = Signal(dict)
    def __init__(self, parent, probeName):
        super(Channel, self).__init__(parent)
        self.probeDict = ChanHandler.singleton.probes[probeName]
        self.name = probeName
        self.loggerTextState    = None
        self.loggerEventState   = None
        self.rrdFiles           = dict()
        self.rrdEnabled         = False

        # BEGIN rrd2 synchro
        self._tmpXmlFiles       = dict()
        self._rrdFiles          = dict()
        self._rrdFilesReady     = dict()
        self._rrdUpdatesPending = dict()
        # END rrd2 synchro

    def delayedRrdRestore(self, reply):
        if (reply['reply']['status'] == 'ok'):
            index = reply['data']
            del self._tmpXmlFiles[index]
            self._rrdFilesReady[index] = True
            self._restorePendingUpdates(index)
        else:
            print "rrdtool restore failed: ", msg

    def _restorePendingUpdates(self, index):
        if index in self._rrdUpdatesPending:
            update = self._rrdUpdatesPending[index].popleft()
            updateString = "update %s %s %s" % (
                self._rrdFiles[index].fileName(),
                self._rrdUpdateString,
                update)
            norrd.cmd(
                updateString,
                callback=self._restorePendingUpdatesContinue,
                data=index)
            return
        dumpMsg = dict()
        dumpMsg['msgType']  = 'probeDump'
        dumpMsg['logger']   = 'bmonitor_logger_rrd2'
        dumpMsg['data']     = (index, self._rrdFiles[index].fileName)
        self.signal.emit(dumpMsg)

    def _restorePendingUpdatesContinue(self, msg):
        index = msg['data']
        if len(self._rrdUpdatesPending[index]) == 0:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'bmonitor_logger_rrd2'
            dumpMsg['data']     = (index, self._rrdFiles[index].fileName)
            self.signal.emit(dumpMsg)
            print "succcccccccesss! restorependingupdatescontinue"
            return

        update = self._rrdUpdatesPending[index].popleft()
        updateString = "update %s %s %s" % (
            self._rrdFiles[index].fileName(),
            self._rrdUpdateString(),
            update)
        norrd.cmd(
            updateString,
            callback=self._restorePendingUpdatesContinue,
            data=index)


    def delayedSyncEvent(self, reply):
        if (reply['success'] == True):
            xmlFile = reply['outfile']
            for key in self._tmpXmlFiles.keys():
                if (self._tmpXmlFiles[key] == xmlFile):
                    index = key
            print "index is ", index
            rrdFile = QTemporaryFile(self)
            rrdFile.open()
            rrdFile.close()
            rrdFileName = rrdFile.fileName()
            self._rrdFiles[index] = rrdFile
            norrd.cmd(
                "restore %s %s --force-overwrite" % (xmlFile, rrdFileName),
                callback = self.delayedRrdRestore,
                data = index
            )
        else:
            print "supercast requestUrl failed: ", reply

    def synchronizeView(self, view):
        if self.loggerTextState != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'bmonitor_logger_text'
            dumpMsg['data']     = self.loggerTextState
            view.handleProbeEvent(dumpMsg)
        if self.rrdEnabled == True:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'bmonitor_logger_rrd'
            dumpMsg['data']     = self.rrdFiles
            view.handleProbeEvent(dumpMsg)
        if self.loggerEventState != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'monitor_events'
            dumpMsg['data']     = self.loggerEventState
            view.handleProbeEvent(dumpMsg)
        
    def handleDump(self, msg):
        dumpType = msg['value']['logger']
        data     = msg['value']['data']
        if   dumpType == 'bmonitor_logger_text':
            self.loggerTextState = deque(data.split('\n'))
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = self.loggerTextState
            self.signal.emit(dumpMsg)
        elif dumpType == 'bmonitor_logger_events':
            self.loggerEventState = msg['value']['data']
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = self.loggerEventState
            self.signal.emit(dumpMsg)
        elif dumpType == 'bmonitor_logger_rrd2':
            self._initRrdUpdate()
            path = msg['value']['path']
            urls = msg['value']['indexes']
            for index in urls.keys():
                xmlFile = QTemporaryFile(self)
                xmlFile.open()
                xmlFile.close()
                fileName = xmlFile.fileName()
                self._tmpXmlFiles[index] = fileName
                self._rrdFiles[index] = None
                self._rrdFilesReady[index] = False
                request = dict()
                request['url']      = "%s/%s" % (path, urls[index])
                request['callback'] = self.delayedSyncEvent
                request['outfile']  = fileName
                supercast.requestUrl(request)

        elif dumpType == 'bmonitor_logger_rrd':
            self.rrdEnabled = True
            # special dump comme in multiple pieces.
            fileId = msg['value']['fileId']
            rrdFile = QTemporaryFile(self)
            rrdFile.open()
            rrdFile.write(str(data))
            rrdFile.close()
            fileName = rrdFile.fileName()
            self.rrdFiles[fileId] = fileName
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'bmonitor_logger_rrd'
            dumpMsg['data']     = dict()
            dumpMsg['data']['fileId'] = fileId
            dumpMsg['data']['file']   = fileName
            self.signal.emit(dumpMsg)
        else:
            print "unknown dump type ", dumpType

    def handleRrdLoggerEvent(self, msg):
        updates = msg['value']['updates']
        for key in updates.keys():
            self._maybeUpdateRrd(key, updates[key])

    def _initRrdUpdate(self):
        self._rrdUpdateString = self.probeDict['loggers']['bmonitor_logger_rrd']['rrdUpdate']

    def _maybeUpdateRrd(self, key, updateString):
        if (self._rrdFilesReady[key] == False):
            if key in self._rrdUpdatesPending:
                self._rrdUpdatesPending[key].append(updateString)
                return
            else:
                self._rrdUpdatesPending[key] = deque()
                self._rrdUpdatesPending[key].append(updateString)
                return
        updateString = "update %s %s %s" % (
            self._rrdFiles[key].fileName(),
            self._rrdUpdateString,
            updateString)
        norrd.cmd(updateString, callback = self.getRrdStatus, data=key)

    def getRrdStatus(self, reply):
        status  = reply['reply']['status']
        index   = reply['data']
        if status == 'ok':
            updateMsg = dict()
            updateMsg['msgType'] = 'rrdProbeEvent'
            updateMsg['logger']  = 'bmonitor_logger_rrd2'
            updateMsg['data']    = index
            self.signal.emit(updateMsg)
        else:
            print "rrdtool update error: ", reply

    def handleReturn(self, msg):
        if self.rrdEnabled == True:
            self._updateRrdDb(msg)
        if self.loggerTextState != None:
            self._updateLoggerText(msg)
        self.signal.emit(msg)

    def handleEvent(self, msg):
        self.loggerEventState.append(msg['value']['data'])
        self.signal.emit(msg)

    def _updateLoggerText(self, msg):
        self.loggerTextState.append(msg['value']['originalRep'])
        if len(self.loggerTextState) > 50:
            self.loggerTextState.popleft()

    def _updateRrdDb(self, msg):
        rrdConf   = self.probeDict['loggers']['bmonitor_logger_rrd']
        rrdFiles  = self.rrdFiles
        keyVals   = msg['value']['keyVals']
        for rrd in rrdFiles.keys():
            updateString = rrdConf[rrd]['update']
            for bind in rrdConf[rrd]['binds']:
                macro   = rrdConf[rrd]['binds'][bind]
                try:
                    value = keyVals[bind]
                except KeyError:
                    print "missing bind. I will not update the rrd"
                    break
                updateString = updateString.replace(macro, str(value))

            template    = re.findall(r'--template\s+[^\s]+',  updateString)
            template    = re.sub(r'--template\s+', r'', template[0])
            rrdvalues   = re.findall(r'N:[^\s]+', updateString)
            rrdvalues   = rrdvalues[0]
            commandString = 'update %s --template %s %s' % (rrdFiles[rrd], template, rrdvalues)
            norrd.cmd(commandString, None)



class AbstractChannelWidget(NFrameContainer):
    def __init__(self, parent, channel):
        super(AbstractChannelWidget, self).__init__(parent)
        print "ABS: init...."
        self.__channel = channel
        self.__connected = False

    def connectProbe(self):
        print "ABS: connect to probe"
        ChanHandler.singleton.subscribe(self, self.__channel)
        self.__connected = True

    def handleProbeEvent(self, msg): 
        print self, ":you should handle this message: ", msg['msgType']

    def __disconnectProbe(self):
        print "ABS: disconnect probe"
        ChanHandler.singleton.unsubscribe(self, self.__channel)

    def destroy(self):
        print "ABS: destroy"
        if self.__connected == True: self.__disconnectProbe()
        self.deleteLater()



class SimpleSignal(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(SimpleSignal, self).__init__(parent)
