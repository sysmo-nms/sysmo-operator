from    PyQt5.QtNetwork    import QTcpSocket, QAbstractSocket
from    PyQt5.QtCore       import (
        Qt,
        QThread, 
        QObject,
        QDataStream,
        QByteArray,
        QIODevice,
        pyqtSignal
)

import sys
import json

def encode(pyTerm):
    jsonStr = json.dumps(pyTerm)
    jsonBin = jsonStr.encode('utf-8')
    return jsonBin

def decode(jsonBin):
    jsonStr = jsonBin.decode('utf-8')
    pyTerm  = json.loads(jsonStr)
    return pyTerm

class SupercastSocket(QObject):
    mQueue      = pyqtSignal(tuple)
    # datas queue from self to Supercast()
    # tuple: (key, payload)
    def __init__(self, parent=None):
        super(SupercastSocket, self).__init__()

        self._nextBlockSize = 0
        self._headerLen     = 4
        self._errorHandler  = None

    def _initializeSocket(self):
        self._socket = QTcpSocket()
        self._socket.connected.connect(self._socketConnected)
        self._socket.readyRead.connect(self._socketReadyRead)
        self._socket.error.connect(self._socketErrorEvent, Qt.DirectConnection)

    def _handleServerMessage(self, payload):
        message = decode(payload)
        self.mQueue.emit(('message', message))

    def _socketConnected(self):
        self.mQueue.emit(('socketConnected', None))

    def _socketErrorEvent(self, event):
        self.mQueue.emit(('socketError', int(event)))

    def _handleClientMessage(self, msg):
        (key, payload) = msg
        if key == 'tryconnect':
            (server, port) = payload
            self._socket.connectToHost(server, port)
        elif key == 'reset':
            self._socket.close()
        elif key == 'authResp':
            (name, password) = payload
            pdu = {
                'from': 'supercast',
                'type': 'authResp',
                'value': {
                    'name':     name,
                    'password': password}
            }
            self._sendToServer(encode(pdu))
        elif key == 'subscribe':
            (queryId, channel) = payload
            pdu = {
                'from': 'supercast',
                'type': 'subscribe',
                'value': {
                    'queryId': queryId,
                    'channel': channel
                }
            }
            self._sendToServer(encode(pdu))
        elif key == 'unsubscribe':
            (queryId, channel) = payload
            pdu = {
                'from': 'supercast',
                'type': 'unsubscribe',
                'value': {
                    'queryId': queryId,
                    'channel': channel
                }
            }
            self._sendToServer(encode(pdu))
        elif key == None:
            pdu = payload
            self._sendToServer(encode(pdu))
        else:
            print("unknown key for mQueue", key)
        

    def _sendToServer(self, pdu):
        request = QByteArray()
        stream  = QDataStream(request, QIODevice.WriteOnly)
        stream.writeUInt32(0)
        stream.writeRawData(pdu)
        stream.device().seek(0)
        stream.writeUInt32(request.size() - 4)
        self._socket.write(request)

    def _socketReadyRead(self):
        stream  = QDataStream(self._socket)

        while stream.atEnd() != True:
            if self._nextBlockSize == 0:
                if self._socket.bytesAvailable() < self._headerLen:
                    return
                self._nextBlockSize = stream.readUInt32()
            if self._socket.bytesAvailable() < self._nextBlockSize:
                return
    
            payload = stream.readRawData(self._nextBlockSize)
            self._nextBlockSize = 0
            self._handleServerMessage(payload)

