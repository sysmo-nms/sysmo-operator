from    PyQt5.QtNetwork    import QTcpSocket
from    PyQt5.QtCore       import (
        QThread, 
        QObject,
        QDataStream,
        QByteArray,
        QIODevice,
        pyqtSignal
)

from    supercast.pdu       import (
        decode,
        encode
)

import sys
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
        self._socket.error.connect(self._socketErrorEvent)

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
            self._socket.connectToHost(server, port)
        elif key == 'authResp':
            (name, passw) = payload
            pdu = encode('authResp', (name, passw))
            self._sendToServer(pdu)
        else:
            pdu = encode(key, payload)
            if pdu == False: return
            else: self._sendToServer(pdu)

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
