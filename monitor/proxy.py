from    PyQt5.QtCore import QObject, pyqtSignal, QTemporaryFile, QDir
from    sysmo_widgets import NFrameContainer
import  supercast.main as supercast
import  sysmapi
import  pyrrd4j
import  os


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
        elif    msg['type'] == 'nchecksDumpMessage':
            self.masterpyqtSignalsDict['nchecksDumpMessage'].signal.emit(msg)
        elif    msg['type'] == 'nchecksUpdateMessage':
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
        self._rrd4jReady = False
        self._rrd4jWait  = list()
        self.probeDict = ChanHandler.singleton.probes[probeName]
        self.name = probeName
        
    def handleReturn(self, msg):
        if self.loggerTextState != None:
            self._updateLoggerText(msg)
        self.signal.emit(msg)

    def handleNchecksDump(self,msg):
        httpDir = msg['value']['httpDumpDir']
        rrdFile = msg['value']['rrdFile']
        rrd4jFile = NTempFile(self)
        rrd4jFile.open()
        rrd4jFile.close()
        self._rrd4jFileName = rrd4jFile.fileName()

        # prevent garbage collection?
        self._ncheckRrdFile = rrd4jFile

        request = dict()
        request['url']      = "%s/%s" % (httpDir, rrdFile)
        request['callback'] = self._handleNchecksDump2nd
        request['outfile']  = self._rrd4jFileName
        supercast.requestUrl(request)
        
    def _handleNchecksDump2nd(self, msg):
        if msg['success'] == True: 
            dumpMsg = dict()
            dumpMsg['type']     = 'nchecksDumpMessage'
            dumpMsg['file']     = msg['outfile']
            self.signal.emit(dumpMsg)
        if len(self._rrd4jWait) == 0:
            self._rrd4jReady = True
        else:
            up = self.rrd4jWait.pop()
            self._doUpdateRrd(self, up)

    def handleNchecksUpdate(self, msg):
        if self._rrd4jReady == False:
            self._rrd4jWait.append(msg)
        else:
            self._doUpdateRrd(msg)
        
    def _doUpdateRrd(self, msg):
        print("do update!!!!!!")
        upKV    = msg['value']['rrdupdates']
        rrdFile = self._rrd4jFileName
        ts      = msg['value']['timestamp']
        update  = dict()
        update['updates']   = upKV
        update['file']      = rrdFile
        update['timestamp'] = ts
        pyrrd4j.update(update, self._doUpdateRrdReply)
        

    def _doUpdateRrdReply(self, reply):
        print("doupdatereply: " + reply)
        self.signal.emit({'type': 'nchecksUpdateMessage'})
        if len(self._rrd4jWait) == 0:
            self._rrd4jReady = True
        else:
            msg = self._rrd4jWait.pop()
            self._doUpdateRrd(msg)


class AbstractChannelWidget(NFrameContainer):
    def __init__(self, parent, channel):
        super(AbstractChannelWidget, self).__init__(parent)
        print("ABS: init....")
        self.__channel = channel
        self.__connected = False

    def connectProbe(self):
        print("ABS: connect to probe")
        ChanHandler.singleton.subscribe(self, self.__channel)
        self.__connected = True

    def handleProbeEvent(self, msg): 
        print((self, ":you should handle this message: ", msg['type']))

    def __disconnectProbe(self):
        print("ABS: disconnect probe")
        ChanHandler.singleton.unsubscribe(self, self.__channel)

    def destroy(self):
        print("ABS: destroy")
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

