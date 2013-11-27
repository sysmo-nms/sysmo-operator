from    PySide.QtCore   import *
from    Supercast       import Link


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
        self.sc         = Link.singleton
        self.sc.setMessageProcessor('modTrackerPDU', self.handleMsg)
        self.masterChan = 'target-MasterChan'

        # common signals from master channel
        self.masterSignalsDict = dict()
        self.masterSignalsDict['probeInfo']     = ChannelSignal(self)
        self.masterSignalsDict['targetInfo']    = ChannelSignal(self)
        self.masterSignalsDict['probeModInfo']  = ChannelSignal(self)

        # common signals from treeview
        self.treeSignalsDict = dict()
        self.treeSignalsDict['select'] = ChannelSignal(self)


    def handleMsg(self, msg):
        if      msg['msgType'] == 'authAck':
            self._autoSubscribe()
        elif    msg['msgType'] == 'probeInfo':
            self.masterSignalsDict['probeInfo'].signal.emit(msg)
        elif    msg['msgType'] == 'targetInfo':
            self.masterSignalsDict['targetInfo'].signal.emit(msg)
        elif    msg['msgType'] == 'probeModInfo':
            self.masterSignalsDict['probeModInfo'].signal.emit(msg)
        elif    msg['msgType'] == 'subscribeOk':
            self._handleSubscribeOk(msg)
        elif    msg['msgType'] == 'unSubscribeOk':
            self._handleUnsubscribeOk(msg)
        else: print "msg received", msg
            

    def _handleSubscribeOk(self, msg):
        print "subscribe ok ", msg

    def _handleUnsubscribeOk(self, msg):
        print "unsubscribe ok ", msg

    def _autoSubscribe(self):
        self.sc.subscribe(self.masterChan)

class ChannelSignal(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(ChannelSignal, self).__init__(parent)
