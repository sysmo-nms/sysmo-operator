from    PyQt5.QtGui            import QIcon
from    PyQt5.QtWidgets        import (
    QDialog,
    QLineEdit,
    QSpinBox,
    QDialogButtonBox,
    QPushButton,
    QFrame,
    QFormLayout,
    QGridLayout,
    QMessageBox,
    QProgressDialog
)
from    PyQt5.QtSvg        import QSvgWidget
import  sysmapi

class Query(QDialog):
    def __init__(self, parent, uncle):
        super(Query, self).__init__(parent)
        self.setMinimumWidth(500)

        self._uncle     = uncle
        self.callback   = uncle.tryConnect

        self._prog = QProgressDialog(self)
        self._prog.setMinimum(0)
        self._prog.setMaximum(0)
        self._prog.hide()
        self._prog.canceled.connect(self._uncle.resetConn)

        # dev shortcuts
        autoName    = 'admin'
        autoPass    = 'password'
        autoPort    = 8888
        autoHost    = 'localhost'


        # edit area
        self.nameLineEdit   = QLineEdit(self)
        self.nameLineEdit.setText(autoName)

        self.passLineEdit   = QLineEdit(self)
        self.passLineEdit.setEchoMode(QLineEdit.Password)
        self.passLineEdit.setText(autoPass)

        self.serverLineEdit = QLineEdit(self)
        self.serverLineEdit.setText(autoHost)

        self.serverPortEdit = QSpinBox(self)
        self.serverPortEdit.setRange(1, 65535)
        self.serverPortEdit.setValue(autoPort)


        formFrame   = QFrame(self)
        formLayout  = QFormLayout(formFrame)
        formLayout.addRow(self.tr("&Server:"),      self.serverLineEdit)
        formLayout.addRow(self.tr("&Port:"),        self.serverPortEdit)
        formLayout.addRow(QFrame(self))
        formLayout.addRow(self.tr("&User Name:"),        self.nameLineEdit)
        formLayout.addRow(self.tr("&Password:"),    self.passLineEdit)
        formFrame.setLayout(formLayout)


        # button area
        ok = QPushButton(
            #QIcon(sysmapi.nGetPixmap('applications-development')),
            self.tr("&Log In"),
            self)
        ok.setDefault(True)
        ok.clicked.connect(self.tryValidate)

        ko = QPushButton(
            #QIcon(sysmapi.nGetPixmap('process-stop')),
            self.tr("&Close"),
            self)
        ko.clicked.connect(self._loginAbort)

        buttons = QDialogButtonBox(self)
        buttons.addButton(ok,   QDialogButtonBox.RejectRole)
        buttons.addButton(ko,   QDialogButtonBox.ApplyRole)


        # graphic area
        svgImage = QSvgWidget(sysmapi.nGetImage('weather-showers'), self)
        svgImage.setFixedSize(150, 150)


        # LAYOUT
        grid = QGridLayout(self)
        grid.addWidget(formFrame,   0,1)
        grid.addWidget(svgImage,    0,0)
        grid.addWidget(buttons,     1,0,1,2)
        self.setLayout(grid)
        self.show()

    def _loginAbort(self):
        self._uncle.loginAbort()
        
    def tryValidate(self):
        tryDict = dict()
        tryDict['name']     = self.nameLineEdit.text()
        tryDict['pass']     = self.passLineEdit.text()
        tryDict['server']   = self.serverLineEdit.text()
        tryDict['port']     = self.serverPortEdit.value()
        self.callback(tryDict)
        self._prog.setLabelText("Trying to log in on server %s:%i" % (tryDict['server'], tryDict['port']))
        self.hide()
        self._prog.show()

    def authError(self, msg):
        self._prog.hide()
        self._prog.deleteLater()
        msgbox = QMessageBox(self)
        msgbox.setText("Login failure!")
        msgbox.setInformativeText("Your user name and password does not match any known user on the server side. Maybe you have mispeled your password?")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setModal(True)
        msgbox.exec_()       
        self.show()
        self._uncle.resetConn()

    def hideAll(self):
        self._prog.hide()
        self.hide()

    def retry(self):
        self._prog.hide()
        self.show()

    def tcpConnected(self, state): pass

    def supConnected(self, state): pass

    def end(self):
        self._prog.hide()
        self.hide()
