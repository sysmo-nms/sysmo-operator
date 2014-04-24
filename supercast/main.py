#!/usr/bin/env python2
import  time
import  sys

from    PySide.QtNetwork    import *
from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    supercast.pdu       import decode, encode
import  supercast.login

def send(pduType, message, callback):
    Supercast.singleton.send(pduType, message, callback)

class Supercast(QObject):

    eventSignals = Signal(tuple)
    # datas (key, other) where key = 'success' | 'abort'

    lQueue      = Signal(tuple)
    # datas queue from self to SupercastSocket()
    # tuple: (key, payload)

    def __init__(self, parent, mainwindow=None):
        super(Supercast, self).__init__(parent)
        Supercast.singleton = self

        # parent of dialogs must be a QMainWindow()
        if mainwindow == None:
            self._mainwindow = parent
        else:
            self._mainwindow = mainwindow

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
        self._queries           = dict()
        self.setMessageProcessor('modSupercastPDU', self._handleSupercastPDU)

    # from client to socket
    def setMessageProcessor(self, fromKey, pyCallable):
        self._mpd.update({fromKey: pyCallable})

    def subscribe(self,   callback, channel):
        queryId = self._getQueryId(callback)
        self.lQueue.emit(('subscribe', (queryId, channel)))

    def unsubscribe(self, callback, channel):
        queryId = self._getQueryId(callback)
        self.lQueue.emit(('unsubscribe', (queryId, channel)))

    def send(self, pduType, message, callback):
        queryId = self._getQueryId(callback)
        self.lQueue.emit((pduType, (queryId, message)))

    def _getQueryId(self, pyCallable):
        queryId = 0
        while True:
            if queryId not in self._queries:
                self._queries[queryId] = pyCallable
                return queryId
            else:
                queryId = queryId + 1

    def _queryNotify(self, msg):
        queryId = msg['queryId']
        caller  = self._queries[queryId]
        caller(msg)
        del self._queries[queryId]

    # from socket
    def _handleThreadMsg(self, msg):
        (msgType, payload) = msg
        if msgType == 'message':
            handler = self._mpd.get(payload['from'])
            if (handler == None):
                hasQueryId = False
                for key in payload.keys(): 
                    if key == 'queryId':
                        hasQueryId = True
                        break
                if hasQueryId == False:
                    print "unknown destination", payload['from']
                else:
                    self._queryNotify(payload)
            else:
                handler(payload)
        elif msgType == 'socketConnected':
            self._setTcpConn(True)
        elif msgType == 'socketError':
            self._handleSocketError(payload)

    def _handleSocketError(self, event):
        if   event == QAbstractSocket.ConnectionRefusedError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.RemoteHostClosedError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.HostNotFoundError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.SocketAccessError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.SocketResourceError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.SocketTimeoutError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.DatagramTooLargeError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.NetworkError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.AddressInUseError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.SocketAddressNotAvailableError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.UnsupportedSocketOperationError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.SslHandshakeFailedError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.UnfinishedSocketOperationError:
            self._showErrorBox(event)
        elif event == QAbstractSocket.UnknownSocketError:
            self._showErrorBox(event)
        else:
            self._showErrorBox(event)


    def _handleSupercastPDU(self, msg):
        msgType = msg['msgType']
        if (msgType == 'authReq'):
            self._setSupConn(True)
            self.serverAuthProto = msg['value']
            self.lQueue.emit(('authResp', (self.userName, self.userPass)))
        elif (msgType == 'authAck'):
            self._setUserConn(True)
            self.groups = msg['value']['groups']
            for item in msg['value']['chans']:
                self._handleChanInfo(item)
        elif (msgType == 'subscribeOk'):
            self._subscribeSuccess(msg['value'])
            self._queryNotify(msg)
        elif (msgType == 'unsubscribeOk'):
            self._unsubscribeSuccess(msg['value'])
            self._queryNotify(msg)
        elif (msgType == 'subscribeErr'):
            self._queryNotify(msg)
        elif (msgType == 'unsubscribeErr'):
            self._queryNotify(msg)
        else:
            print "handle other?", msgType

    def _subscribeSuccess(self, chan):
        self.activeChannels.append(chan)

    def _unsubscribeSuccess(self, chan):
        self.activeChannels.remove(chan)

    def _handleChanInfo(self, item):
        if (item['eventType'] == 'create'):
            self.staticChans.update({item['channelId']: None})
            msg = dict()
            msg['msgType']  = 'staticChanInfo'
            msg['event']    = item['eventType']
            msg['value']    = item['channelId']
            self._broadcast(msg)

    def _broadcast(self, msg):
        for key in self._mpd:
            if key == 'modSupercastPDU': pass
            else:
                handler = self._mpd.get(key)
                handler(msg)

    ###########################
    # LOG IN AND MESSAGES BOX #
    ###########################
    def tryLogin(self):
        # parent must be QMainWindow, but callbacks must be self.
        parent = self._mainwindow
        uncle  = self
        self._loginWin = supercast.login.Query(parent, uncle)

    def loginAbort(self):
        self.eventSignals.emit(('abort', None))

    def tryConnect(self, cred):
        self.userName   = cred['name']
        self.userPass   = cred['pass']
        self.server     = cred['server']
        self.port       = cred['port']
        self.lQueue.emit(('tryconnect', (self.server, self.port)))

    def _setTcpConn(self, state):
        if state == True:
            self._loginWin.tcpConnected(True)
        else:
            self._loginWin.tcpConnected(False)

    def _setSupConn(self, state):
        if state == True:
            self._loginWin.supConnected(True)
        else:
            self._loginWin.supConnected(False)

    def _setUserConn(self, state):
        self.eventSignals.emit(('success', None))
        self._loginWin.close()

    def _showErrorBox(self, event):
        msgBox = QMessageBox(self._mainwindow)
        msgBox.setText("Socket ERROR %s" % event)
        msgBox.setStandardButtons(QMessageBox.Close)
        msgBox.exec_()
        self.eventSignals.emit(('abort', None))

    #########
    # CLOSE #
    #########
    def supercastClose(self):
        self._thread.quit()


class SupercastSocket(QThread):
    mQueue      = Signal(tuple)
    # datas queue from self to Supercast()
    # tuple: (key, payload)
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
        self.mQueue.emit(('socketConnected', None))

    def _socketErrorEvent(self, event):
        self.mQueue.emit(('socketError', event))

    def _handleClientMessage(self, msg):
        (key, payload) = msg
        if key == 'tryconnect':
            (server, port) = payload
            self.socket.connectToHost(server, port)
        elif key == 'authResp':
            (name, passw) = payload
            pdu = encode('authResp', (name, passw))
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
