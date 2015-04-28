from    PyQt5.QtGui            import QIcon, QPixmap
from    PyQt5.QtWidgets        import (
    QLabel,
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
from    PyQt5.QtCore       import pyqtSignal
import  sysmapi
from sysmo_widgets import NFrameContainer, NGridContainer
from sysmo_images import getPixmap

class LogInDialog(QDialog):
    loginPressed = pyqtSignal(dict)
    def __init__(self, ref, parent=None):
        QDialog.__init__(self, parent)
        #self.setFixedWidth(350)
        self._ref = ref

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


        serverFrame = QFrame(self)
        serverLay = QGridLayout(serverFrame)
        serverLay.setContentsMargins(0,0,0,0)
        serverLay.addWidget(self.serverLineEdit,            0,0)
        serverLay.addWidget(QLabel('Port:', serverFrame),  0,1)
        serverLay.addWidget(self.serverPortEdit,            0,2)
        serverLay.setColumnStretch(0,1)
        serverLay.setColumnStretch(1,0)
        serverLay.setColumnStretch(2,0)

        sep = QFrame(self)
        sep.setFixedHeight(15)

        formFrame   = QFrame(self)
        formLayout  = QFormLayout(formFrame)
        formLayout.setContentsMargins(0,0,0,0)
        formLayout.addRow(self.tr("&User Name:"),   self.nameLineEdit)
        formLayout.addRow(self.tr("&Password:"),    self.passLineEdit)
        formLayout.addRow(sep)
        formLayout.addRow(self.tr("&Server:"), serverFrame)
        formFrame.setLayout(formLayout)

        # button area
        ok = QPushButton(
            self.tr("&Log In"),
            self)
        ok.setDefault(True)
        ok.clicked.connect(self._tryValidate)

        ko = QPushButton(
            self.tr("&Close"),
            self)
        ko.clicked.connect(self.reject)

        buttons = QDialogButtonBox(self)
        buttons.addButton(ok,   QDialogButtonBox.RejectRole)
        buttons.addButton(ko,   QDialogButtonBox.ApplyRole)


        banner = QLabel(self)
        pix = getPixmap("operator-banner")
        ret = banner.setPixmap(pix)
        print("ret: " + str(ret) + "  " + str(pix) + " " + str(banner.pixmap()))
        # LAYOUT

        fr = NFrameContainer(self)
        grid = QGridLayout(fr)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(22)

        grid.addWidget(banner,      0,0)
        grid.addWidget(formFrame,   1,0)
        grid.addWidget(buttons,     2,0)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,0)
        gr = NGridContainer(self)
        gr.addWidget(banner)
        gr.addWidget(fr)

    def _tryValidate(self):
        tryDict = dict()
        tryDict['name']     = self.nameLineEdit.text()
        tryDict['pass']     = self.passLineEdit.text()
        tryDict['server']   = self.serverLineEdit.text()
        tryDict['port']     = self.serverPortEdit.value()
        self.accept()
        self.loginPressed.emit(tryDict)
