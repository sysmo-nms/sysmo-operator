#!/usr/bin/env python2
import  time
import  sys

from    PySide.QtNetwork    import *
from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    SupercastPDU        import decode, encode

class Link(QTcpSocket):
    def __init__(self, parent=None):
        super(Link, self).__init__(parent)

        Link.singleton = self

        # public  variables access
        self.userName   = ''
        self.userPass   = ''
        self.groups     = []
        self.server     = ''
        self.port       = 8888
        self.activeChannels     = []
        self.serverAuthProto    = ''
        self.staticChans        = dict()

        # private variables
        self._mpd           = dict()
        self._nextBlockSize = 0
        self._headerLen     = 4

        self.connected.connect(self._socketConnected)
        self.readyRead.connect(self._socketReadyRead)
        self.disconnected.connect(self._socketDisconnected)
        self.error.connect(self._socketErrorEvent)
        self.setMessageProcessor('modSupercastPDU', self._handleSupercastPDU)

    ###################
    # PUBLIC  METHODS #
    ###################
    def setMessageProcessor(self, fromKey, function):
        self._mpd.update({fromKey: function})

    def tryConnect(self):
        self.connectToHost(self.server, self.port)

    def subscribe(self, channel):
        pdu = encode('subscribe', channel)
        self.sendToServer(pdu)

    def unsubscribe(self, channel):
        pdu = encode('unsubscribe', channel)
        self.sendToServer(pdu)


    def sendToServer(self, pdu):
        request = QByteArray()
        stream = QDataStream(request, QIODevice.WriteOnly)
        stream.writeUInt32(0)
        stream.writeRawData(pdu)
        stream.device().seek(0)
        stream.writeUInt32(request.size() - 4)
        self.write(request)

    ###################
    # PRIVATE METHODS #
    ###################
    def _socketReadyRead(self):
        stream  = QDataStream(self)

        while stream.atEnd() != True:
            if self._nextBlockSize == 0:
                if self.bytesAvailable() < self._headerLen:
                    return
                self._nextBlockSize = stream.readUInt32()
            if self.bytesAvailable() < self._nextBlockSize:
                return
    
            payload = stream.readRawData(self._nextBlockSize)
            self._nextBlockSize = 0
            self._handleServerMessage(payload)

    def _socketConnected(self): pass

    def _socketDisconnected(self):
        print "socket is disconnected"

    def _socketErrorEvent(self, event):
        print "error event is: ", event

    # MESSAGES HANDLING
    def _handleServerMessage(self, msg):
        message = decode(msg)
        handler = self._mpd.get(message['from'])
        if (handler == None):
            print "pdu to unknown destination", message['from']
        else:
            handler(message)

    def _handleSupercastPDU(self, msg):
        msgType = msg['msgType']
        if (msgType == 'authReq'):
            self.serverAuthProto = msg['value']
            pdu = encode(
                'authResp',
                userId      = self.userName,
                password    = self.userPass
            )
            self.sendToServer(pdu)
        elif (msgType == 'authAck'):
            self.groups = msg['value']['groups']
            for item in msg['value']['chans']:
                self._handleChanInfo(msg, item)
        elif (msgType == 'subscribeOk'):
            self._subscribeSuccess(msg['value'])
            self._broadcast(msg)
        elif (msgType == 'unsubscribeOk'):
            self._broadcast(msg)
        else:
            print "handle other", msgType

    def _unsubscribeSuccess(self, chan):
        self.activeChannels.remove(chan)

    def _subscribeSuccess(self, chan):
        self.activeChannels.append(chan)

    def _handleChanInfo(self, msg, item):
        if (item['eventType'] == 'create'):
            self.staticChans.update({item['channelId']: None})
            self._broadcast(msg)

    def _broadcast(self, msg):
        for key in self._mpd:
            if key == 'modSupercastPDU': pass
            else:
                handler = self._mpd.get(key)
                handler(msg)
