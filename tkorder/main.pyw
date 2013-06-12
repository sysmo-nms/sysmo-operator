#!/usr/bin/env python2
import  sys, time
from    supercast   import decode, encode
from    PySide      import QtCore, QtGui, QtNetwork

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

###########################################################################
###########################################################################
## MAIN WINDOWS ###########################################################
###########################################################################
###########################################################################
class SupercastClient(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SupercastClient, self).__init__(parent)

        " MainWindow "
        self.setObjectName(_fromUtf8("MainWindow"))
        self.resize(400, 300)
        self.setCentralWidget(SupercastClientMain(self))

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
        self.initSocket()
        self.initMpd()

        " End init "
        self.updateStatusBar("Started!")


    #######################################################################
    # SUPERCAST (socket methods and client auth)                          #
    #######################################################################
    def initSocket(self):
        # default
        self.setSocketServer('localhost')
        self.setSocketPort(8888)
        self.initSocketAuthVals()
        
        self.tcpSocket      = QtNetwork.QTcpSocket()
        self.tcpSocket.connected.connect(self.socketConnected)
        self.tcpSocket.readyRead.connect(self.socketReadyRead)
        self.tcpSocket.disconnected.connect(self.socketDisconnected)
        self.tcpSocket.error.connect(self.socketErrorEvent)

    def initSocketPduCtrl(self):
        self.header_len     = 4
        self.header_data    = QtCore.QByteArray()
        self.payload_len    = 0
        self.payload_data   = QtCore.QByteArray()

    def initSocketAuthVals(self):
        self.userName   = ''
        self.userPass   = ''

    def initMpd(self):
        self.mpd = dict()
        self.setMessageProcessor('modSupercastPDU', self.handleSupercastPDU)

    def setSocketAuthUser(self, userName):
        self.userName = userName

    def setSocketAuthPass(self, password):
        self.userPass = password

    def setSocketServer(self, server):
        self.server = server

    def setSocketPort(self, port):
        self.port   = port


    def setMessageProcessor(self, fromKey, function):
        self.mpd.update({fromKey: function})

    def connect(self):
        self.initSocketPduCtrl()
        self.tcpSocket.connectToHost(self.server, self.port)

    def handleServerMessage(self, msg):
        message = decode(msg)
        handler = self.mpd.get(message['from'])
        handler(message)

    def handleSupercastPDU(self, msg):
        print "hello, handlesupercastpdu message is ", msg
        msgType = msg['msgType']
        if msgType == 'authReq':
            self.serverAuthProto = msg['value']
            pdu = encode(
                'authResp',
                userId=self.userName,
                password=self.userPass
            )
            self.sendToServer(pdu)
        else:
            print "handle other"

    def sendToServer(self, pdu):
        p = QtCore.QByteArray().fromHex(hex(len(pdu))).rightJustified(4, '\0')
        p.append(pdu)
        self.tcpSocket.write(p)
        #print "send message: ", p.size(), len(pdu)

    " SERVER EVENTS "
    " four bytes header to unpack before reading the payload "
    def socketReadyRead(self):
        print "hhhhhhhhhhhhhhhhhhhhhh"
        ha = self.header_data.size()
        hl = self.header_len

        while 1:
            if (ha != hl):
                self.header_data.append(self.tcpSocket.readData(hl - ha))
                if (self.header_data.size() == hl):
                    (self.payload_len, True) = self.header_data.toHex().toInt()
                    print "ERROR IS HERE WHEN: (0, False)"
                    print "header complete, now read data: ", self.header_data.toHex().toInt()
                    self.payload_data.append(
                        self.tcpSocket.readData(self.payload_len))
                    if (self.payload_data.size() == self.payload_len):
                        self.handleServerMessage(self.payload_data)
                        self.initSocketPduCtrl()
                        if self.tcpSocket.bytesAvailable() == 0: break
            else:
                self.payload_data.append(
                    self.tcpSocket.readData(
                        self.payload_size - self.payload_data.size() ) )
                print "header complete 1"
                self.debugPduCtrl()
                if (self.payload_data.size() == self.payload_len):
                    print "payload complete 1"
                    self.debugPduCtrl()
                    self.handleServerMessage(self.payload_data)
                    self.initSocketPduCtrl()
                    if self.tcpSocket.bytesAvailable() == 0: break
            

    def debugPduCtrl(self):
        print "ici: ", self.header_data.size(), " ", self.header_len
        print "ela: ", self.payload_data.size(), " ", self.payload_len

    def socketConnected(self):
        print "socket is connected"
        self.updateStatusBar("Connected!")

    def socketDisconnected(self):
        print "socket is disconnected"
        self.updateStatusBar("disconnected!")

    def socketErrorEvent(self, event):
        print "error event is: ", event





    #######################################################################
    # SELF.STATUSBAR methods                                              #
    #######################################################################
    def updateStatusBar(self, msg):
        self.statusBar.showMessage(msg)

###########################################################################
###########################################################################
## LOG IN DIALOG ##########################################################
###########################################################################
###########################################################################
class SupercastLogInDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        print "auto log in will come here"
        super(SupercastLogInDialog, self).__init__(parent)

        self.setWindowTitle("Log in to Supercast/ENMS server")

        myGrid  = QtGui.QGridLayout()

        self.serverLabel   = QtGui.QLabel("Server:", self)
        self.serverName     = QtGui.QLineEdit(self)
        self.serverPort     = QtGui.QSpinBox(self)
        self.serverPort.setMinimum(1)
        self.serverPort.setMaximum(65535)

        self.userNameLabel = QtGui.QLabel("User name:", self)
        self.passWordLabel = QtGui.QLabel("Password:", self)
        self.userName   = QtGui.QLineEdit(self)

        self.passWord   = QtGui.QLineEdit(self)
        self.passWord.setEchoMode(QtGui.QLineEdit.Password)

        self.saveCredentials = QtGui.QCheckBox("Remember me", self)

        self.logInButton    = QtGui.QPushButton("LogIn")
        self.logInButton.setDefault(True)

        self.cancelButton   = QtGui.QPushButton("Cancel")

        self.buttonBox      = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.logInButton,
            QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton,
            QtGui.QDialogButtonBox.DestructiveRole)

        myGrid.addWidget(self.serverLabel,      0, 0)
        myGrid.addWidget(self.serverName,       0, 1)
        myGrid.addWidget(self.serverPort,       0, 2)
        myGrid.addWidget(self.userNameLabel,    1, 0)
        myGrid.addWidget(self.userName,         1, 1, 1, 2)
        myGrid.addWidget(self.passWordLabel,    2, 0)
        myGrid.addWidget(self.passWord,         2, 1, 1, 2)
        myGrid.addWidget(self.saveCredentials,  3, 0, 1, 3)
        myGrid.addWidget(self.buttonBox,        4, 0, 1, 3)
        myGrid.setColumnMinimumWidth(1, 250)

        self.connect(
            self.logInButton,
            QtCore.SIGNAL("clicked()"), 
            self.logInPushed
        )
        self.connect(
            self.cancelButton,
            QtCore.SIGNAL("clicked()"), 
            self.cancelPushed
        )

        self.setLayout(myGrid)

    def logInPushed(self):
        host    = self.serverName.text()
        port    = self.serverPort.value()
        user    = self.userName.text()
        passwd  = self.passWord.text()

        #self.supercastClient.setSocketAuthUser(user)
        #self.supercastClient.setSocketAuthPass(passwd)
        #self.supercastClient.setSocketServer(host)
        #self.supercastClient.setSocketPort(port)

        self.supercastClient.setSocketAuthUser('admuser')
        self.supercastClient.setSocketAuthPass('passwd')
        self.supercastClient.setSocketServer('localhost')
        self.supercastClient.setSocketPort(8888)
        self.supercastClient.connect()
        self.supercastClient.show()
        self.splash.close()
        self.close()
        
    def cancelPushed(self):
        self.close()

    def setSupercastClient(self, supercastClient):
        self.supercastClient = supercastClient

    def setSplash(self, splashScreen):
        self.splash = splashScreen
        self.splash.show()






class SupercastClientMain(QtGui.QTabWidget):
    def __init__(self, parent):
        super(SupercastClientMain, self).__init__(parent)
        self.addTab(QtGui.QLabel("TRACKER HERE", self), 'Tracker')
        self.addTab(QtGui.QLabel("MAPS", self), 'Maps')
        self.setTabPosition(QtGui.QTabWidget.West)
        self.setMovable(True)
        self.setUsesScrollButtons(True)
        self.setTabShape(QtGui.QTabWidget.Rounded)



def main():
    supercastApp    = QtGui.QApplication(sys.argv)

    splash_pixmap   = QtGui.QPixmap("/home/seb/Images/overcast2.png")
    splash          = QtGui.QSplashScreen(splash_pixmap)
    
    supercastUi     = SupercastClient()

    loginUi         = SupercastLogInDialog()
    loginUi.setSupercastClient(supercastUi)
    loginUi.setSplash(splash)
    loginUi.show()

    sys.exit(supercastApp.exec_())

if __name__ == "__main__":
    main()
