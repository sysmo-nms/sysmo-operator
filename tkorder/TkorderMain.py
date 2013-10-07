#!/usr/bin/env python2
import  time
import  sys

from    PySide      import QtCore, QtGui, QtNetwork
from    TkorderPDU  import decode, encode
import  ModTracker
from  TkorderIcons  import TkorderIcons
import  TkorderCentral

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
    @classmethod
    def setSingleton(cls, obj):
        cls.singleton = obj

    @classmethod
    def singleton(cls):
        return cls.singleton

    def __init__(self, parent=None):
        super(SupercastClient, self).__init__(parent)

        " This is a singleton. Can be accessed here "
        SupercastClient.setSingleton(self)
        TkorderIcons.init()

        " MainWindow "
        self.setObjectName(_fromUtf8("MainWindow"))
        self.resize(400, 300)

        " Status bar "
        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)

        " Menu bar "
        exitAction  = QtGui.QAction(TkorderIcons.get('system-log-out'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        menu        = self.menuBar()
        menuFile    = menu.addMenu('Engage')
        menuFile.addAction(exitAction)

        " Server connexion and socket related "
        self.initSocket()
        self.initMpd()

        " Server channel info "
        self.initChanInfos()
        self.autoSubscribe = True

        " User group info "
        self.initGroupsInfos()

        " End init "
        self.setCentralWidget(TkorderCentral.TkorderCentralWidget(self))
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

    def initChanInfos(self):
        self.chanDb = dict()

    def initGroupsInfos(self):
        self.groupList = list()

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
        if (handler == None):
            print "pdu to unknown destination", message['from']
        else:
            handler(message)

    def handleSupercastPDU(self, msg):
        msgType = msg['msgType']
        if (msgType == 'authReq'):
            self.serverAuthProto = msg['value']
            pdu = encode(
                'authResp',
                userId=self.userName,
                password=self.userPass
            )
            self.sendToServer(pdu)
        elif (msgType == 'authAck'):
            self.setGroups(msg['value']['groups'])
            for item in msg['value']['chans']:
                self.handleChanInfo(item)
        elif (msgType == 'subscribeOk'):
            pass
        else:
            print "handle other", msgType

    def handleChanInfo(self, msg):
        if (msg['eventType'] == 'create'):
            self.chanDb.update({msg['channelId']: None})
            if (self.autoSubscribe == True):
                pdu = encode('subscribe', msg['channelId'])
                self.sendToServer(pdu)
                

    def setGroups(self, msg):
        self.groupList = msg

    def sendToServer(self, pdu):
        p = QtCore.QByteArray().fromHex(hex(len(pdu))).rightJustified(4, '\0')
        p.append(pdu)
        self.tcpSocket.write(p)

    " SERVER EVENTS "
    " four bytes header to unpack before reading the payload "
    def socketReadyRead(self):
        ha = self.header_data.size()
        hl = self.header_len

        while 1:
            if (ha != hl):
                self.header_data.append(self.tcpSocket.readData(hl - ha))
                if (self.header_data.size() == hl):
                    self.payload_len = int(str(self.header_data.toHex()), 16)
                    self.payload_data.append(
                        self.tcpSocket.readData(self.payload_len)
                    )
                    if (self.payload_data.size() == self.payload_len):
                        self.handleServerMessage(self.payload_data)
                        self.initSocketPduCtrl()
                        if self.tcpSocket.bytesAvailable() == 0:
                            break
            else:
                self.payload_data.append(
                    self.tcpSocket.readData(
                        self.payload_len - self.payload_data.size()
                    )
                )
                if (self.payload_data.size() == self.payload_len):
                    self.handleServerMessage(self.payload_data)
                    self.initSocketPduCtrl()
                    if self.tcpSocket.bytesAvailable() == 0:
                        break

    def socketConnected(self):
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
# TODO QFormLayout a la place du grid
class SupercastLogInDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SupercastLogInDialog, self).__init__(parent)

        self.setWindowTitle("Log in to Supercast/ENMS server")

        myGrid  = QtGui.QGridLayout(self)

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
        self.supercastClient.setSocketServer('192.168.0.9')
        self.supercastClient.setSocketPort(8888)

        self.supercastClient.connect()
        self.supercastClient.show()
        self.close()
        
    def cancelPushed(self):
        self.close()

    def setSupercastClient(self, supercastClient):
        self.supercastClient = supercastClient



def main(arguments):
    supercastApp    = QtGui.QApplication(arguments)
    supercastUi     = SupercastClient()
    supercastApp.setWindowIcon(TkorderIcons.get('applications-development'))
    loginUi         = SupercastLogInDialog()

    loginUi.setSupercastClient(supercastUi)
    loginUi.show()

    sys.exit(supercastApp.exec_())
