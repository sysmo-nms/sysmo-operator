from PySide.QtGui   import (
    QWizard,
    QWizardPage,
    QLabel,
    QVBoxLayout,
    QCommandLinkButton,
    QButtonGroup,
    QFormLayout,
    QCheckBox,
    QFrame,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QPushButton,
    QGroupBox,
    QTreeWidget,
    QTreeWidgetItem,
    QMessageBox
)
from PySide.QtCore import Qt

from noctopus_widgets import NGrid, NFrame, NGridContainer, NFrameContainer
import nocapi
import opus.monitor.api as monapi
import supercast.main   as supercast


class Page1(QWizardPage):
    SNMP_V2  = 0
    SNMP_V3  = 1
    IP_V4    = 0
    IP_V6    = 1
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('Create a network element'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network element to the main configuration
        '''))
        self.setFinalPage(True)
        self._initLayout()

    def _initLayout(self):
        layout = NGrid(self)

        layout.addWidget(self._initMain(),         0,0)
        self.setLayout(layout)

    def _initMain(self):
        tempFrame   = NFrame(self)
        tempLayout  = NGrid(tempFrame)
        tempLayout.setVerticalSpacing(20)
        tempLayout.setRowStretch(1,0)
        tempFrame.setLayout(tempLayout)
        self._ipLine    = QLineEdit(self)
        self._ipButton  = QComboBox(self)
        self._ipButton.insertItem(self.IP_V4, 'IP version 4:')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6:')
        self._ipButton.setFocusPolicy(Qt.ClickFocus)

        self._snmpButton = QComboBox(self)
        self._snmpButton.insertItem(self.SNMP_V2, 'SNMP version 2b')
        self._snmpButton.insertItem(self.SNMP_V3, 'SNMP version 3')
        self._snmpButton.setFocusPolicy(Qt.ClickFocus)

        tempLayout.addWidget(self._ipButton,                            0,0)
        tempLayout.addWidget(self._ipLine,                              0,1)
        tempLayout.addWidget(self._snmpButton,                          1,0)
        tempLayout.addWidget(self._initSnmpFrame(),                     1,1,2,1)

        tempLayout.setAlignment(self._snmpButton, Qt.AlignVCenter)
        tempLayout.setColumnStretch(0,0)
        tempLayout.setColumnStretch(1,1)
        return tempFrame

    def _initSnmpFrame(self):
        snmpFrame = QGroupBox(self)
        snmpFrame.setContentsMargins(0,0,0,0)
        snmpFrame.setTitle(self.tr("&SNMP v2b configuration"))
        snmpLayout = QFormLayout(snmpFrame)
        snmpFrame.setLayout(snmpLayout)
        self._snmpV2Write = QLineEdit(snmpFrame)
        self._snmpV2Read  = QLineEdit(snmpFrame)

        snmpLayout.insertRow(0, self.tr('Write community:'), self._snmpV2Write)
        snmpLayout.insertRow(1, self.tr('Read community:'),  self._snmpV2Read)
        return snmpFrame

    def nextId(self):
        return -1

    def validatePage(self):
        snmpV2Read  = self._snmpV2Read.text()
        snmpV2Write = self._snmpV2Write.text()
        ipAddress   = self._ipLine.text()

        snmpVersion = self._snmpButton.currentIndex()
        ipVersion   = self._ipButton.currentIndex()
        print "snmp version is ", snmpVersion, " ip ", ipVersion

        perms       = (["admin"], ["admin"])
        tpl         = "Generic SNMP element"

        if self._assertCmd(
            snmpVersion,
            ipVersion,
            snmpV2Read,
            snmpV2Write,
            ipAddress
        ):
            print "true?"
            ret = supercast.send(
                'monitorCreateTarget', 
                (
                    ipAddress,
                    perms,
                    snmpV2Read,
                    snmpV2Write,
                    tpl
                ),
                self.monitorReply
            )

        #self.dial = QMessageBox(self)
        #self.dial.setModal(True)
        #self.dial.setText(self.tr('Waiting for server response'))
        #button = self.dial.buttons()
        #button.setDisabled(True)
        #self.dial.exec_()
        return False

    def _assertCmd(self, a,b,c,d,e): return True
    def monitorReply(self, msg):
        print "get reply!!!!!!", msg
