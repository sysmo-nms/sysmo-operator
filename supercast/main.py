from    PySide.QtCore import (
    QObject,
    QThread,
    Signal,
    Qt
)
from    supercast.http_manager  import SupercastAccessManager
from    supercast.socket        import SupercastSocket
import  supercast.login

def send(pduType, message, callback):
    Supercast.singleton.send(pduType, message, callback)

def requestUrl(request):
    Supercast.singleton.httpManager.requestUrl(request)

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

        self.httpManager = None
        self._thread = QThread(self)
        self._socketThread     = SupercastSocket()
        # datas from SupercastSocket() to self
        # tuple: (key, payload)
        self._socketThread.mQueue.connect(
            self._handleThreadMsg,
            Qt.QueuedConnection)

        # datas from self to SupercastSocket()
        self.lQueue.connect(
            self._socketThread._handleClientMessage,
            Qt.QueuedConnection
        )

        # init socket thread
        self._thread.started.connect(self._socketThread._initializeSocket)
        self._socketThread.moveToThread(self._thread)
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

    def _extendedQueryNotify(self, msg):
        queryId = msg['queryId']
        caller  = self._queries[queryId]
        caller(msg)
        lastPdu = msg['lastPdu']
        if (lastPdu == True):
            del self._queries[queryId]

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
                if 'queryId' in payload:
                    if 'lastPdu' in payload:
                        self._extendedQueryNotify(payload)
                    else:
                        self._queryNotify(payload)
                else:
                    print "unknown destination", payload['from']

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
        if (msgType == 'serverInfo'):
            self._setSupConn(True)
            self.serverAuthProto    = msg['authProto']
            self.dataPort           = msg['dataPort']
            self.dataProto          = msg['dataProto']
            self._initHttpManager()
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

    def _initHttpManager(self):
        self.httpManager = SupercastAccessManager(
                self, self.server, self.dataProto, self.dataPort)

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
        if (self._thread.wait(5000) != True):
            self._thread.terminate();
            if (self._thread.wait(5000) != True):
                print "failed to close supercast socket thread"
        if (self.httpManager != None):
            self.httpManager.terminateAll()
