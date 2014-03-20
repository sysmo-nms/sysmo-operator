#!/usr/bin/env python2
import  time
import  sys

from    PySide.QtNetwork    import *
from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    SupercastPDU        import decode, encode

class Supercast(QObject):

    lQueue = Signal(tuple)
    # datas queue from self to SupercastSocket()
    # tuple: (key, payload)

    def __init__(self, parent, eventHandler):
        super(Supercast, self).__init__(parent)
        self._eventHandler = eventHandler
        self._thread     = SupercastSocket(self)
        # datas from SupercastSocket() to self
        # tuple: (key, payload)
        self._thread.mQueue.connect(
            self._handleThreadMsg,
            Qt.QueuedConnection)
        self._thread.start()
        self.userName   = ''
        self.userPass   = ''
        self.groups     = []
        self.server     = ''
        self.port       = 8888
        self.activeChannels     = []
        self.serverAuthProto    = ''
        self.staticChans        = dict()
        self._mpd               = dict()
        self.setMessageProcessor('modSupercastPDU', self._handleSupercastPDU)

    # from client to socket
    def setMessageProcessor(self, fromKey, pyCallable):
        self._mpd.update({fromKey: pyCallable})

    def setEventHandler(self, pyCallable):
        self._eventHandler = pyCallable

    def tryConnect(self):
        self.lQueue.emit(('tryconnect', (self.server, self.port)))

    def subscribe(self, channel):
        # TODO include an id in the call, and associate it with a callable.
        self.lQueue.emit(('subscribe', channel))

    def unsubscribe(self, channel):
        # TODO include an id in the call, and associate it with a callable.
        self.lQueue.emit(('unsubscribe', channel))

    # from socket
    def _handleThreadMsg(self, msg):
        (msgType, payload) = msg
        print "message is ", payload, self._mpd
        if msgType == 'message':
            handler = self._mpd.get(payload['from'])
            if (handler == None):
                print "unknown destination", payload['from']
            else:
                handler(payload)

    def _handleSupercastPDU(self, msg):
        msgType = msg['msgType']
        if (msgType == 'authReq'):
            self.serverAuthProto = msg['value']
            self.lQueue.emit(('authResp', (self.userName, self.userPass)))
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
            print "handle other?", msgType

    def _unsubscribeSuccess(self, chan):
        self.activeChannels.remove(chan)

    def _unsubscribeSuccess(self, chan):
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

    def close(self):
        self._thread.quit()


class SupercastSocket(QThread):
    mQueue      = Signal(tuple)
    def __init__(self, parent=None):
        super(SupercastSocket, self).__init__(parent)
        self._client = parent
        # datas from parent to self
        # tuple: (key, payload)
        self._client.lQueue.connect(
            self._handleClientMessage,
            Qt.QueuedConnection
        )

        self._nextBlockSize = 0
        self._headerLen     = 4
        self._errorHandler  = None

    def start(self):
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self._socketConnected)
        self.socket.readyRead.connect(self._socketReadyRead)
        self.socket.error.connect(self._socketErrorEvent)
        QThread.start(self)

    def _handleServerMessage(self, payload):
        message = decode(payload)
        self.mQueue.emit(('message', message))

    def _socketConnected(self):
        self.mQueue.emit(('socketConnected', ''))

    def _socketErrorEvent(self, event):
        self.mQueue.emit(('socketError', message))

    def _handleClientMessage(self, msg):
        (key, payload) = msg
        if key == 'tryconnect':
            (server, port) = payload
            self.socket.connectToHost(server, port)
        elif key == 'authResp':
            (name, passw) = payload
            pdu = encode(key, userId=name, password=passw)
            self._sendToServer(pdu)
        else:
            pdu = encode(key, payload)
            self._sendToServer(pdu)

    def _sendToServer(self, pdu):
        request = QByteArray()
        stream  = QDataStream(request, QIODevice.WriteOnly)
        stream.writeUInt32(0)
        stream.writeRawData(pdu)
        stream.device().seek(0)
        stream.writeUInt32(request.size() - 4)
        self.socket.write(request)

    def _socketReadyRead(self):
        stream  = QDataStream(self.socket)

        while stream.atEnd() != True:
            if self._nextBlockSize == 0:
                if self.socket.bytesAvailable() < self._headerLen:
                    return
                self._nextBlockSize = stream.readUInt32()
            if self.socket.bytesAvailable() < self._nextBlockSize:
                return
    
            payload = stream.readRawData(self._nextBlockSize)
            self._nextBlockSize = 0
            self._handleServerMessage(payload)

