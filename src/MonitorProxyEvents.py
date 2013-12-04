from    PySide.QtCore   import *
import  Supercast


class ChannelHandler(QObject):
    
    " This class handle other widgets subscription and emit message "
    " received by the server with Signal(). The method 'handleMSG' receive "
    " messages from the server "
    " She is also responsible of the channel group concept and max channel "
    " limitations."

    def __init__(self, parent, maxChans=3):
        super(ChannelHandler, self).__init__(parent)
        # simple init
        ChannelHandler.singleton = self
        self.sc         = Supercast.Link.singleton
        self.sc.setMessageProcessor('modTrackerPDU', self.handleMsg)
        self.masterChan = 'target-MasterChan'
        
        # register handle probeInfo and targetInfo
        self.targets    = dict()
        self.probes     = dict()

        # channel handling
        self.subscribedChans    = list()
        self.pendingSubscribe   = list()
        self.chanProxy          = dict()

        # signals
        self.masterSignalsDict = dict()
        self.masterSignalsDict['probeInfo']     = SimpleSignal(self)
        self.masterSignalsDict['targetInfo']    = SimpleSignal(self)
        self.masterSignalsDict['probeModInfo']  = SimpleSignal(self)
        self.masterSignalsDict['probeDump']     = SimpleSignal(self)
        self.masterSignalsDict['probeReturn']   = SimpleSignal(self)

        # connect myself
        self.masterSignalsDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self.masterSignalsDict['targetInfo'].signal.connect(self._handleTargetInfo)
        self.masterSignalsDict['probeDump'].signal.connect(self._handleProbeDump)
        self.masterSignalsDict['probeReturn'].signal.connect(self._handleProbeReturn)
        # END

    def subscribe(self, viewObject, channel):
        if channel in self.subscribedChans:
            self.chanProxy[channel].synchronizeView(viewObject)
            self.chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
        elif channel in self.pendingSubscribe:
            self.chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
        else:
            self.chanProxy[channel] = Channel(self, channel)
            self.chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
            self._subscribe(channel)

    def unsubscribe(self, viewObject, channel):
        self.chanProxy[channel].signal.disconnect(viewObject.handleProbeEvent)

    def _subscribe(self, channel):
        self.pendingSubscribe.append(channel)
        self.sc.subscribe(channel)

    def _unsubscribe(self, channel):
        self.pendingUnsubscribe.append(channel)
        self.sc.unsubscribe(channel)

    def _handleSubscribeOk(self, msg):
        channel = msg['value']
        if channel == self.masterChan: return
        self.pendingSubscribe.remove(channel)
        self.subscribedChans.append(channel)

    def _handleUnsubscribeOk(self, msg):
        channel = msg['value']
        if channel == self.masterChan: return
        self.chanSignals[channel].destroy()
        del self.chanSignals[channel]

    def _handleProbeDump(self, msg):
        channel = msg['value']['id']
        self.chanProxy[channel].handleDump(msg)

    def _handleProbeReturn(self, msg):
        channel = msg['value']['id']
        self.chanProxy[channel].handleReturn(msg)

    def _autoSubscribe(self):
        self.sc.subscribe(self.masterChan)

    def _handleProbeInfo(self, msg):
        probeInfo   = msg['value']
        probeName   = probeInfo['name']
        self.probes[probeName] = probeInfo

    def _handleTargetInfo(self, msg):
        targetInfo  = msg['value']
        targetName  = targetInfo['name']
        self.targets[targetName] = targetInfo

    def handleMsg(self, msg):
        if      msg['msgType'] == 'probeReturn':
            self.masterSignalsDict['probeReturn'].signal.emit(msg)
        elif    msg['msgType'] == 'probeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)
        elif    msg['msgType'] == 'probeInfo':
            self.masterSignalsDict['probeInfo'].signal.emit(msg)
        elif    msg['msgType'] == 'targetInfo':
            self.masterSignalsDict['targetInfo'].signal.emit(msg)
        elif    msg['msgType'] == 'probeModInfo':
            self.masterSignalsDict['probeModInfo'].signal.emit(msg)
        elif    msg['msgType'] == 'authAck':
            self._autoSubscribe()
        elif    msg['msgType'] == 'subscribeOk':
            self._handleSubscribeOk(msg)
        elif    msg['msgType'] == 'unSubscribeOk':
            self._handleUnsubscribeOk(msg)
        else: 
            print "unknown msg received", msg['msgType']

class Channel(QObject):
    signal = Signal(dict)
    def __init__(self, parent, probeName):
        super(Channel, self).__init__(parent)
        self.name = probeName
        self.loggerTextState = None
        self.rrdFile = None
        self.rrdFileName = None

    def synchronizeView(self, view):
        if self.loggerTextState != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'btracker_logger_text'
            dumpMsg['data']     = self.loggerTextState
            view.handleProbeEvent(dumpMsg)
        if self.rrdFile != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'btracker_logger_rrd'
            dumpMsg['data']     = self.rrdFileName
            view.handleProbeEvent(dumpMsg)
        
    def handleDump(self, msg):
        dumpType = msg['value']['logger']
        data     = msg['value']['data']
        if   dumpType == 'btracker_logger_text':
            self.loggerTextState = data
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = data
            self.signal.emit(dumpMsg)
        elif dumpType == 'btracker_logger_rrd':
            self.rrdFile = QTemporaryFile(self)
            self.rrdFile.open()
            self.rrdFile.write(data)
            self.rrdFile.close()
            self.rrdFileName = self.rrdFile.fileName()
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = self.rrdFileName
            self.signal.emit(dumpMsg)

    def handleReturn(self, msg):
        self.signal.emit(msg)

class TextDump(QObject):
    def __init__(self, parent):
        super(TextDump, self).__init__(parent)

class RrdDump(QObject):
    def __init__(self, parent):
        super(RrdDump, self).__init__(parent)


class SimpleSignal(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(SimpleSignal, self).__init__(parent)

