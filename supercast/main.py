from    PyQt5.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    Qt
)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QAbstractSocket
from supercast.http_manager  import SupercastAccessManager
from supercast.socket        import SupercastSocket
import sys

def send(message, callback):
    Supercast.singleton.send(message, callback)

def requestUrl(request):
    Supercast.singleton.httpManager.requestUrl(request)

class Supercast(QObject):

    events = pyqtSignal(tuple)
    # datas (key, other) where key = 'success' | 'abort'

    lQueue      = pyqtSignal(tuple)
    # datas queue from self to SupercastSocket()
    # tuple: (key, payload)

    def __init__(self, parent):
        super(Supercast, self).__init__(parent)
        Supercast.singleton = self

        self.httpManager = None
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
        self._thread = QThread()
        self._thread.started.connect(self._socketThread._initializeSocket)
        self._socketThread.moveToThread(self._thread)
        self._thread.start()

        self._socketPlusUserOk = False

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
        self.setMessageProcessor('supercast', self._handleSupercastPDU)

    # from client to socket
    def setMessageProcessor(self, fromKey, pyCallable):
        self._mpd.update({fromKey: pyCallable})

    def subscribe(self,   callback, channel):
        print("subscribe? " + str(channel))
        queryId = self._getQueryId(callback)
        self.lQueue.emit(('subscribe', (queryId, channel)))

    def unsubscribe(self, callback, channel):
        queryId = self._getQueryId(callback)
        self.lQueue.emit(('unsubscribe', (queryId, channel)))

    def send(self, message, callback):
        message['value']['queryId'] = self._getQueryId(callback)
        self.lQueue.emit((None, message))

    def _getQueryId(self, pyCallable):
        queryId = 0
        while True:
            if queryId not in self._queries:
                self._queries[queryId] = pyCallable
                return queryId
            else:
                queryId = queryId + 1

    def _extendedQueryNotify(self, msg):
        queryId = msg['value']['queryId']
        caller  = self._queries[queryId]
        caller(msg)
        lastPdu = msg['value']['lastPdu']
        if (lastPdu == True):
            del self._queries[queryId]

    def _queryNotify(self, msg):
        queryId = msg['value']['queryId']
        caller  = self._queries[queryId]
        caller(msg)
        del self._queries[queryId]

    # from socket
    def _handleThreadMsg(self, msg):
        (msgType, payload) = msg
        if msgType == 'message':
            handler = self._mpd.get(payload['from'])
            if (handler == None):
                if 'queryId' in payload['value']:
                    if 'lastPdu' in payload['value']:
                        self._extendedQueryNotify(payload)
                    else:
                        self._queryNotify(payload)
                else:
                    print(("unknown destination", payload['from']))

            else:
                handler(payload)
        elif msgType == 'socketConnected':
            self.events.emit(('tcpConnected',True))
        elif msgType == 'socketError':
            errorEvent = self._getSocketError(payload)
            self.events.emit(('socketError', errorEvent))
        else:
            print("handle unknown event" + str(msgType))

    def _getSocketError(self, event):
        if   event == QAbstractSocket.ConnectionRefusedError:
            a = "The connection was refused by the peer."
            b = "You may trying to connect to the wrong host, or the wrong port."
        elif event == QAbstractSocket.RemoteHostClosedError:
            a = "The remote host closed the connexion."
            b = "This can append if the host come down, or if the service is restarting."
        elif event == QAbstractSocket.HostNotFoundError:
            a = "Host not found"
            b = "This host is not know by your DNS"
        elif event == QAbstractSocket.SocketTimeoutError:
            a = "Socket timed out"
            b = "Is your network connexion down?"
        elif event == QAbstractSocket.NetworkError:
            a = "Network error"
            b = "Does your network cable pluged in?"
        else:
            a = "Socket Error"
            b = "Error code: %i" % event
        return (a,b)

    def _handleSupercastPDU(self, msg):
        msgType = msg['type']
        if (msgType == 'serverInfo'):
            self.serverAuthProto    = msg['value']['authType']
            self.dataPort           = msg['value']['dataPort']
            self.dataProto          = msg['value']['dataProto']
            self._initHttpManager()
            self.lQueue.emit(('authResp', (self.userName, self.userPass)))
        elif (msgType == 'authAck'):
            self.events.emit(('success', None))
            self.groups = msg['value']['groups']
            for channel in msg['value']['staticChans']:
                self._handleChanInfo(channel)
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
        elif (msgType == 'authErr'):
            self.events.emit(('authErr',msg))
        else:
            print(("handle other?", msgType))

    def _initHttpManager(self):
        self.httpManager = SupercastAccessManager(
                self, self.server, self.dataProto, self.dataPort)

    def _subscribeSuccess(self, chan):
        self.activeChannels.append(chan)

    def _unsubscribeSuccess(self, chan):
        self.activeChannels.remove(chan)

    def _handleChanInfo(self, channel):
        msg = {
            'type':  'staticChanInfo',
            'value': channel
        }
        self._broadcast(msg)

    def _broadcast(self, msg):
        for key in self._mpd:
            if key == 'supercast': pass
            else:
                handler = self._mpd.get(key)
                handler(msg)

    ##########
    # LOG IN #
    ##########
    def tryConnect(self, cred):
        self.userName   = cred['name']
        self.userPass   = cred['pass']
        self.server     = cred['server']
        self.port       = cred['port']
        self.lQueue.emit(('tryconnect', (self.server, self.port)))

    def resetConn(self):
        self.lQueue.emit(('reset', None))


    #########
    # CLOSE #
    #########
    def supercastClose(self):
        self._thread.quit()
        if (self._thread.wait(5000) != True):
            self._thread.terminate();
            if (self._thread.wait(5000) != True):
                print("failed to close supercast socket thread")
        if (self.httpManager != None):
            self.httpManager.terminateAll()
