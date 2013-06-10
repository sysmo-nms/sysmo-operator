#!/usr/bin/env python2
import  sys, time
from    supercast   import decode, encode
from    PySide      import QtCore, QtGui, QtNetwork

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class SupercastClient(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SupercastClient, self).__init__(parent)

        " MainWindow "
        self.setObjectName(_fromUtf8("MainWindow"))
        self.resize(400, 300)
        self.setCentralWidget(SupercastClientCenter(self))
        #self.pushButton1    = QtGui.QPushButton("START", self)
        #self.setCentralWidget(self.pushButton1)

        " Status bar "
        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)

        " Menu bar "
        exitAction  = QtGui.QAction(QtGui.QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        menu        = self.menuBar()
        menuFile    = menu.addMenu('Engage')
        menuFile.addAction(exitAction)

        " Server connexion and socket related "
        self.header_len     = 4
        self.header_data    = QtCore.QByteArray()
        self.payload_len    = 0
        self.payload_data   = QtCore.QByteArray()
        self.server         = 'localhost'
        self.port           = 8888
        self.messagesCount  = 0
        self.tcpSocket      = QtNetwork.QTcpSocket()
        self.tcpSocket.connected.connect(self.socketConnected)
        self.tcpSocket.readyRead.connect(self.socketReadyRead)
        self.tcpSocket.disconnected.connect(self.socketDisconnected)
        self.tcpSocket.error.connect(self.socketErrorEvent)
        self.tcpSocket.connectToHost(self.server, self.port)

        " End init "
        self.updateStatusBar("Started!")

    #
    #
    " SELF.SOCKET methods "
    #
    #
    " four bytes header to unpack before reading the payload "
    def socketReadyRead(self):
        ha = self.header_data.size()
        hl = self.header_len

        while 1:
            if (ha != hl):
                self.header_data.append(self.tcpSocket.readData(hl - ha))
                if (self.header_data.size() == hl):
                    (self.payload_len, True) = self.header_data.toHex().toInt()
                    self.payload_data.append(
                        self.tcpSocket.readData(self.payload_len))
                    if (self.payload_data.size() == self.payload_len):
                        self.handleServerMessage(self.payload_data)
                        self.header_data  = QtCore.QByteArray()
                        self.payload_data = QtCore.QByteArray()
                        if self.tcpSocket.bytesAvailable() == 0: break
            else:
                self.payload_data.append(
                    self.tcpSocket.readData(
                        self.payload_size - self.payload_data.size() ) )
                if (self.payload_data.size() == self.payload_len):
                    self.handleServerMessage(self.payload_data)
                    self.header_data  = QtCore.QByteArray()
                    self.payload_data = QtCore.QByteArray()
                    if self.tcpSocket.bytesAvailable() == 0: break
            

    def socketConnected(self):
        print "socket is connected"
        self.updateStatusBar("Connected!")

    def socketDisconnected(self):
        print "socket is disconnected"
        self.updateStatusBar("disconnected!")

    def socketErrorEvent(self, event):
        print "error event is: ", event

    def handleServerMessage(self, msg):
        print "hello, message is ", decode(msg)



    #
    #
    " SELF.STATUSBAR methods "
    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)


class SupercastClientCenter(QtGui.QFrame):
    def __init__(self, parent=None):
        super(SupercastClientCenter, self).__init__(parent)
        self.pushButton1    = QtGui.QPushButton("START", self)

class SupercastClientLeft(QtGui.QFrame):
    def __init__(self, parent=None):
        super(SupercastClientLeft, self).__init__(parent)


if __name__ == "__main__":
    supercastApp    = QtGui.QApplication(sys.argv)
    splash_pixmap   = QtGui.QPixmap("/home/seb/Images/overcast2.png")
    splash          = QtGui.QSplashScreen(splash_pixmap)
    splash.show()

    supercastUi     = SupercastClient()
    splash.finish(supercastUi)
    supercastUi.show()

    sys.exit(supercastApp.exec_())
