#!/usr/bin/env python2
import  time
import  sys

from    PySide.QtNetwork    import *
from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    SupercastPDU        import decode, encode
from    collections         import deque

class Link(QTcpSocket):
    @classmethod
    def subscribe(cls, channel):
        cls.my._subscribeToChannel(channel)

    @classmethod
    def unsubscribe(cls, channel):
        cls.my._unsubscribeFromChannel(channel)

    @classmethod
    def setMaxChannels(cls, maxChans):
        cls.my.maxChans = maxChans

    @classmethod
    def getMaxChannels(cls): 
        return cls.my.maxChans


    @classmethod
    def setMessageProcessor(cls, a, b,):
        cls.my._setMessageProcessor(a, b)


    def __init__(self, parent=None):
        super(Link,self).__init__(parent)
        Link.my = self

        self.nextBlockSize  = 0
        self.headerLen      = 4

        # default
        self.setSocketServer('localhost')
        self.setSocketPort(8888)
        self.maxChans = 2
        self.subscribedChans = deque([])
        self.specialChans   = ['target-MasterChan']

        self.connected.connect(self.socketConnected)
        self.readyRead.connect(self.socketReadyRead)
        self.disconnected.connect(self.socketDisconnected)
        self.error.connect(self.socketErrorEvent)

        self.autoSubscribe = True
        self.userName   = ''
        self.userPass   = ''
        self.groupList = list()
        self.mpd = dict()
        self._setMessageProcessor('modSupercastPDU', self.handleSupercastPDU)
        self.chanDb = dict()

    def setSocketAuthUser(self, userName):
        self.userName = userName

    def setSocketAuthPass(self, password):
        self.userPass = password

    def setGroups(self, msg):
        self.groupList = msg

    def setSocketServer(self, server):
        self.server = server

    def setSocketPort(self, port):
        self.port   = port

    def _setMessageProcessor(self, fromKey, function):
        self.mpd.update({fromKey: function})

    def connectServer(self):
        self.connectToHost(self.server, self.port)

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
                self._handleChanInfo(item)
        elif (msgType == 'subscribeOk'):
            self._subscribeSuccess(msg['value'])
        elif (msgType == 'unsubscribeOk'): pass
        else:
            print "handle other", msgType

    def _handleChanInfo(self, msg):
        if (msg['eventType'] == 'create'):
            self.chanDb.update({msg['channelId']: None})
            if (self.autoSubscribe == True):
                Link.subscribe(msg['channelId'])

    def _subscribeToChannel(self, channel):
        pdu = encode('subscribe', channel)
        self.sendToServer(pdu)

    def _subscribeSuccess(self, chan):
        # is a special chan?
        if chan in self.specialChans: pass
        else:
            q = self.subscribedChans
            m = self.maxChans
            # is allready registered?
            if chan in q: pass
            else:
                if len(q) == m:
                    unsub = q.popleft()
                    self.sendToServer(encode('unsubscribe', unsub))
                    q.append(chan)
                else:
                    q.append(chan)


    def _unsubscribeFromChannel(self, channel):
        pdu = encode('unsubscribe', channel)
        self.sendToServer(pdu)

    def sendToServer(self, pdu):
        request = QByteArray()
        stream = QDataStream(request,
            QIODevice.WriteOnly)
        stream.writeUInt32(0)
        stream.writeRawData(pdu)
        stream.device().seek(0)
        stream.writeUInt32(request.size() - 4)
        self.write(request)

    def socketReadyRead(self):
        stream  = QDataStream(self)

        while stream.atEnd() != True:
            if self.nextBlockSize == 0:
                if self.bytesAvailable() < self.headerLen:
                    return
                self.nextBlockSize = stream.readUInt32()
            if self.bytesAvailable() < self.nextBlockSize:
                return
    
            payload = stream.readRawData(self.nextBlockSize)
            self.nextBlockSize = 0
            self.handleServerMessage(payload)

    def socketConnected(self): pass

    def socketDisconnected(self):
        print "socket is disconnected"

    def socketErrorEvent(self, event):
        print "error event is: ", event

















# TODO
class LogInDialog(QDialog):
    def __init__(self, parent=None):
        super(LogInDialog, self).__init__(parent)
        self.passLineEdit = QLineEdit(self)
        self.nameLineEdit = QLineEdit(self)
        self.serverLineEdit = QLineEdit(self)
        self.serverPortEdit = QSpinBox(self)
        self.setMinimumWidth(500)

        buttons = QDialogButtonBox(self)
        buttons.addButton(QDialogButtonBox.Abort)
        buttons.addButton(QDialogButtonBox.Open)
        buttons.addButton(QDialogButtonBox.Help)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Name:"), self.nameLineEdit)
        formLayout.addRow(self.tr("&Password:"), self.passLineEdit)
        formLayout.addRow(self.tr("&Server:"), self.serverLineEdit)
        formLayout.addRow(self.tr("&Port:"), self.serverPortEdit)
        formLayout.addRow(buttons)
        self.formLayout = formLayout

        self.setLayout(self.formLayout)


class LogInDialog2(QDialog):
    def __init__(self, parent=None):
        super(LogInDialog2, self).__init__(parent)

        self.setWindowTitle("Log in to Supercast/ENMS server")

        # self.progress = QProgressDialog("Connexion.", "Cancel", 0, 100)
        # self.progress.setWindowModality(Qt.WindowModal)
        # self.progress.show()

        myGrid  = QGridLayout(self)

        self.serverLabel   = QLabel("Server:", self)
        self.serverName     = QLineEdit(self)
        self.serverPort     = QSpinBox(self)
        self.serverPort.setMinimum(1)
        self.serverPort.setMaximum(65535)

        self.userNameLabel = QLabel("User name:", self)
        self.passWordLabel = QLabel("Password:", self)
        self.userName   = QLineEdit(self)

        self.passWord   = QLineEdit(self)
        self.passWord.setEchoMode(QLineEdit.Password)

        self.saveCredentials = QCheckBox("Remember me", self)

        self.logInButton    = QPushButton("LogIn")

        self.cancelButton   = QPushButton("Cancel")

        self.buttonBox      = QDialogButtonBox(Qt.Horizontal)
        self.buttonBox.addButton(self.logInButton,
            QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton,
            QDialogButtonBox.DestructiveRole)

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
            SIGNAL("clicked()"), 
            self.logInPushed
        )
        self.connect(
            self.cancelButton,
            SIGNAL("clicked()"), 
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

        Link.my.setSocketAuthUser('admuser')
        Link.my.setSocketAuthPass('passwd')
        Link.my.setSocketServer('192.168.0.9')
        Link.my.setSocketPort(8888)

        Link.my.connectServer()
        self.supercastClient.show()
        self.close()
        
    def cancelPushed(self):
        self.close()

