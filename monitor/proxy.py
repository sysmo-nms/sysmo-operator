from    PyQt5.QtCore import QObject, pyqtSignal, QTemporaryFile, QDir
from    sysmo_widgets import NFrameContainer
import  supercast.main as supercast
import  sysmapi
import  pyrrd4j
import  os

import sys

def pr(val):
    print(str(val))
    sys.stdout.flush()

class ChanHandler(QObject):
    
    " This class handle other widgets subscription and emit message "
    " received by the server with pyqtSignal(). The method 'handleMSG' receive "
    " messages from the server "
    " She is also responsible of the channel group concept and max channel "
    " limitations."

    def __init__(self, parent, maxChans=3):
        super(ChanHandler, self).__init__(parent)
        ChanHandler.singleton = self
        
        sysmapi.nConnectSupercastEnabled(self._initSupercast)

        self._initChanHandling()
        self._initpyqtSignals()

    def _initSupercast(self):
        sysmapi.nSetMessageProcessor('monitor', self.handleSupercastMsg)

    def _initChanHandling(self):
        self._masterChan        = 'target-MasterChan'
        self._subscribedChans   = list()
        self._pendingSubscribe  = list()
        self._chanProxy         = dict()
        self.targets            = dict()
        self.probes             = dict()

    def _initpyqtSignals(self):
        signals = dict()
        signals['infoProbe'] = SimplepyqtSignal(self)
        signals['infoProbe'].signal.connect(self._handleProbeInfo)

        signals['infoTarget'] = SimplepyqtSignal(self)
        signals['infoTarget'].signal.connect(self._handleTargetInfo)

        signals['probeReturn'] = SimplepyqtSignal(self)
        signals['probeReturn'].signal.connect(self._handleProbeReturn)

        signals['deleteTarget'] = SimplepyqtSignal(self)
        signals['deleteTarget'].signal.connect(self._handleDeleteTarget)

        signals['deleteProbe'] = SimplepyqtSignal(self)
        signals['deleteProbe'].signal.connect(self._handleDeleteProbe)

        signals['nchecksDumpMessage'] = SimplepyqtSignal(self)
        signals['nchecksDumpMessage'].signal.connect(self._handleNchecksDump)

        signals['nchecksUpdateMessage'] = SimplepyqtSignal(self)
        signals['nchecksUpdateMessage'].signal.connect(self._handleNchecksUpdate)

        self.masterpyqtSignalsDict = signals

    def handleSupercastMsg(self, msg):
        if      msg['type'] == 'probeReturn':
            self.masterpyqtSignalsDict['probeReturn'].signal.emit(msg)
        elif    msg['type'] == 'infoProbe':
            self.masterpyqtSignalsDict['infoProbe'].signal.emit(msg)
        elif    msg['type'] == 'infoTarget':
            self.masterpyqtSignalsDict['infoTarget'].signal.emit(msg)
        elif    msg['type'] == 'deleteTarget':
            self.masterpyqtSignalsDict['deleteTarget'].signal.emit(msg)
        elif    msg['type'] == 'deleteProbe':
            self.masterpyqtSignalsDict['deleteProbe'].signal.emit(msg)

        elif    msg['type'] == 'nchecksSimpleDumpMessage':
            pr("simple dump?")
            self.masterpyqtSignalsDict['nchecksDumpMessage'].signal.emit(msg)

        elif    msg['type'] == 'nchecksSimpleUpdateMessage':
            self.masterpyqtSignalsDict['nchecksUpdateMessage'].signal.emit(msg)

        elif    msg['type'] == 'nchecksTableDumpMessage':
            self.masterpyqtSignalsDict['nchecksDumpMessage'].signal.emit(msg)

        elif    msg['type'] == 'nchecksTableUpdateMessage':
            self.masterpyqtSignalsDict['nchecksUpdateMessage'].signal.emit(msg)

        elif    msg['type'] == 'staticChanInfo':
            chan    = msg['value']
            if chan == self._masterChan:
                self._autoSubscribe()
        elif    msg['type'] == 'subscribeOk':
            self._handleSubscribeOk(msg)
        elif    msg['type'] == 'unSubscribeOk':
            self._handleUnsubscribeOk(msg)
        else: 
            print(("unknown msg received", msg['type']))

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
        sysmapi.nSubscribe(self.handleSupercastMsg, channel)

    def _unsubscribe(self, channel):
        self.pendingUnsubscribe.append(channel)
        sysmapi.nUnsubscribe(self.handleSupercastMsg, channel)

    def _handleSubscribeOk(self, msg):
        channel = msg['value']['channel']
        if channel == self._masterChan: pass
        self._pendingSubscribe.remove(channel)
        self._subscribedChans.append(channel)

    def _handleUnsubscribeOk(self, msg):
        channel = msg['value']
        if channel == self._masterChan: return
        self.chanpyqtSignals[channel].destroy()
        del self.chanpyqtSignals[channel]

    def _handleNchecksDump(self,msg):
        channel = msg['value']['name']
        self._chanProxy[channel].handleNchecksDump(msg)

    def _handleNchecksUpdate(self,msg):
        channel = msg['value']['name']
        self._chanProxy[channel].handleNchecksUpdate(msg)
        
    def _handleProbeReturn(self, msg):
        channel = msg['value']['name']
        if channel in list(self._chanProxy.keys()):
            self._chanProxy[channel].handleReturn(msg)

    def _handleProbeInfo(self, msg):
        infoProbe   = msg['value']
        probeName   = infoProbe['name']
        self.probes[probeName] = infoProbe

    def _handleTargetInfo(self, msg):
        infoTarget  = msg['value']
        targetName  = infoTarget['name']
        self.targets[targetName] = infoTarget


    def _handleDeleteTarget(self, msg):
        target = msg['value']['name']
        del self.targets[target]

    def _handleDeleteProbe(self, msg):
        probe = msg['value']['name']
        del self.probes[probe]

    # startup subscribe
    def _autoSubscribe(self):
        sysmapi.nSubscribe(self._handleAutoSubscribe, self._masterChan)

    def _handleAutoSubscribe(self, msg):
        if msg['type'] == 'subscribeOk':
            self._masterchanRunning = True
        else:
            print(("error: ", msg))

class Channel(QObject):
    signal = pyqtSignal(dict)
    def __init__(self, parent, probeName):
        super(Channel, self).__init__(parent)
        self.name = probeName
        
    def handleReturn(self, msg):
        self.signal.emit(msg)

    def handleNchecksDump(self,msg):
        if msg['type'] == "nchecksSimpleDumpMessage":
            self._handler = SimpleHandler(self, msg)
        elif msg['type'] == "nchecksTableDumpMessage":
            self._handler = TableHandler(self, msg)
        
    def synchronizeView(self, viewObj):
        self._handler.synchronizeView(viewObj)

    def handleNchecksUpdate(self, msg):
        self._handler.handleUpdate(msg)






class TableHandler(QObject):
    def __init__(self, parent, msg):
        super(TableHandler, self).__init__(parent)
        self._channel = parent

        self._rrd4jReady = dict()
        self._rrd4jWait = list()
        self._rrd4jFileNames = dict()
        
        httpDir  = msg['value']['httpDumpDir']
        rrdFiles = msg['value']['elementToFile']

        for idx in rrdFiles.keys():
            fileName = rrdFiles[idx]
            rrd4jFile = NTempFile(self)
            rrd4jFile.open()
            rrd4jFile.close()
            self._rrd4jFileNames[idx] = rrd4jFile.fileName()
            self._rrd4jReady[idx] = False

            request = dict()
            request['url'] = "%s/%s" % (httpDir, fileName)
            request['callback'] = self._handleDump
            request['outfile'] = self._rrd4jFileNames[idx]
            request['opaque'] = idx
            supercast.requestUrl(request)
            
        pr("tablehandler init" + str(msg))

    def _handleDump(self, msg):
        if msg['success'] == True:
            idx = msg['opaque']
            self._rrd4jReady[idx] = True
            
        if False in self._rrd4jReady.values(): return
        
        dumpMsg = dict()
        dumpMsg['type'] = 'nchecksTableDumpMessage'
        dumpMsg['elementToFile'] = self._rrd4jFileNames
        self._channel.signal.emit(dumpMsg)

        if len(self._rrd4jWait) == 0:
            self._rrd4jReady = True
        else:
            up = self.rrd4jWait.pop()
            self._doUpdateRrd(self, up)
        
    def handleUpdate(self, msg):
        if self._rrd4jReady == False:
            self._rrd4jWait.append(msg)
        else:
            self._doUpdateRrd(msg)

    def _doUpdateRrd(self, msg):
        upKV    = msg['value']['rrdupdates']
        if len(upKV.keys()) == 0: return
        else:
            for idx in upKV.keys():
                rrdFile = self._rrd4jFileNames[idx]
                timestamp = msg['value']['timestamp']
                update = dict()
                update['updates'] = upKV[idx]
                update['file'] = rrdFile
                update['timestamp'] = timestamp
                pyrrd4j.update(update, self._doUpdateRrdReply)

    def _doUpdateRrdReply(self, reply):
        self._channel.signal.emit({'type': 'nchecksTableUpdateMessage'})
        if len(self._rrd4jWait) == 0:
            self._rrd4jReady = True
        else:
            msg = self._rrd4jWait.pop()
            self._doUpdateRrd(msg)

    def synchronizeView(self, viewObj):
        if False not in self._rrd4jFileNames:
            dumpMsg = dict()
            dumpMsg['type'] = 'nchecksTableDumpMessage'
            dumpMsg['elementToFile'] = self._rrd4jFileNames
            self._channel.signal.emit(dumpMsg)
        pr("tablehandler SynchronizeView")









class SimpleHandler(QObject):
    def __init__(self, parent, msg):
        super(SimpleHandler, self).__init__(parent)
        self._channel = parent

        self._rrd4jReady = False
        self._rrd4jWait  = list()
        self._rrd4jFileName  = None

        httpDir = msg['value']['httpDumpDir']
        rrdFile = msg['value']['rrdFile']
        rrd4jFile = NTempFile(self)
        rrd4jFile.open()
        rrd4jFile.close()
        self._rrd4jFileName = rrd4jFile.fileName()

        request = dict()
        request['url']      = "%s/%s" % (httpDir, rrdFile)
        request['callback'] = self._handleDump2nd
        request['outfile']  = self._rrd4jFileName
        supercast.requestUrl(request)

    def _handleDump2nd(self, msg):
        if msg['success'] == True: 
            dumpMsg = dict()
            dumpMsg['type']     = 'nchecksSimpleDumpMessage'
            dumpMsg['file']     = msg['outfile']
            self._channel.signal.emit(dumpMsg)
        if len(self._rrd4jWait) == 0:
            self._rrd4jReady = True
        else:
            up = self.rrd4jWait.pop()
            self._doUpdateRrd(self, up)

    def handleUpdate(self, msg):
        if self._rrd4jReady == False:
            self._rrd4jWait.append(msg)
        else:
            self._doUpdateRrd(msg)
        
    def _doUpdateRrd(self, msg):
        upKV    = msg['value']['rrdupdates']
        if len(upKV.keys()) == 0: return
        else:
            rrdFile = self._rrd4jFileName
            ts      = msg['value']['timestamp']
            update  = dict()
            update['updates']   = upKV
            update['file']      = rrdFile
            update['timestamp'] = ts
            pyrrd4j.update(update, self._doUpdateRrdReply)
        

    def _doUpdateRrdReply(self, reply):
        self._channel.signal.emit({'type': 'nchecksSimpleUpdateMessage'})
        if len(self._rrd4jWait) == 0:
            self._rrd4jReady = True
        else:
            msg = self._rrd4jWait.pop()
            self._doUpdateRrd(msg)

    def synchronizeView(self, viewObj):
        if self._rrd4jReady == True:
            dumpMsg = dict()
            dumpMsg['type'] = 'nchecksSimpleDumpMessage'
            dumpMsg['file'] = self._rrd4jFileName
            viewObj.handleProbeEvent(dumpMsg)


class AbstractChannelWidget(NFrameContainer):
    def __init__(self, parent, channel):
        super(AbstractChannelWidget, self).__init__(parent)
        pr("ABS: init....")
        self.__channel = channel
        self.__connected = False

    def connectProbe(self):
        pr("ABS: connect to probe")
        ChanHandler.singleton.subscribe(self, self.__channel)
        self.__connected = True

    def handleProbeEvent(self, msg): 
        pr((self, ":you should handle this message: ", msg['type']))

    def __disconnectProbe(self):
        pr("ABS: disconnect probe")
        ChanHandler.singleton.unsubscribe(self, self.__channel)

    def destroy(self):
        pr("ABS: destroy")
        if self.__connected == True: self.__disconnectProbe()
        self.deleteLater()



class SimplepyqtSignal(QObject):
    signal = pyqtSignal(dict)
    def __init__(self, parent):
        super(SimplepyqtSignal, self).__init__(parent)

class NTempFile(QTemporaryFile):
    def __init__(self, parent):
        super(NTempFile, self).__init__(parent)
        self.setFileTemplate(
            os.path.join(QDir.tempPath(), 'nc_temp-XXXXXXX')
        )

