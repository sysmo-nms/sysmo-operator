#!/usr/bin/env python2

import sys
import pyasn1

from PySide import QtCore, QtGui, QtNetwork

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

        " Server connexion "
        self.server         = 'localhost'
        self.port           = 8889
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
    def socketReadyRead(self):
        data                = self.tcpSocket.read(1024)
        #data                = self.tcpSocket.readAll() ?
        self.messagesCount += 1
        self.updateStatusBar("Message count: " + str(self.messagesCount))
        print "datas are: ", data

    def socketConnected(self):
        print "socket is connected"
        self.updateStatusBar("Connected!")

    def socketDisconnected(self):
        print "socket is disconnected"
        self.updateStatusBar("disconnected!")

    def socketErrorEvent(self, event):
        print "error event is: ", event

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
    supercastApp = QtGui.QApplication(sys.argv)
    supercastUi  = SupercastClient()
    supercastUi.show()
    sys.exit(supercastApp.exec_())
