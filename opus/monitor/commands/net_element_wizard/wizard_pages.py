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
    QProgressDialog,
    QStackedWidget,
    QProgressBar
)
from PySide.QtCore import Qt

from noctopus_widgets import (
    NGrid,
    NFrame,
    NGridContainer,
    NFrameContainer,
    NIpv4Form,
    NIpv6Form
)

import nocapi
import opus.monitor.api as monapi
import supercast.main   as supercast

SNMP_V3  = 0
SNMP_V2  = 1
IP_V4    = 0
IP_V6    = 1

class Page1(QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('Create a network element'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network element to the main configuration
        '''))
        #self.setFinalPage(True)
        self._initLayout()

    def _initLayout(self):
        layout = NGrid(self)

        layout.addWidget(self._initMain(),         0,0)
        self.setLayout(layout)

    def _initMain(self):
        tempFrame   = NFrameContainer(self)
        tempLayout  = NGridContainer(tempFrame)
        tempLayout.setContentsMargins(0,8,0,8)
        tempLayout.setVerticalSpacing(20)
        tempLayout.setRowStretch(1,0)
        tempFrame.setLayout(tempLayout)


        # ipv4/6 selection and edition
        self._ip4 = NIpv4Form(self)
        self._ip6 = NIpv6Form(self)
        self._ipLine = QStackedWidget(self)
        self._ipLine.setFixedHeight(20)
        self._ipLine.insertWidget(IP_V4, self._ip4)
        self._ipLine.insertWidget(IP_V6, self._ip6)
        self._ipButton  = QComboBox(self)
        self._ipButton.currentIndexChanged[int].connect(self._ipLine.setCurrentIndex)
        self._ipButton.insertItem(IP_V4, 'IP version 4')
        self._ipButton.insertItem(IP_V6, 'IP version 6')
        self._ipButton.setFocusPolicy(Qt.ClickFocus)


        # snmpv2/3 selection and edition
        self._snmp2b = QGroupBox(self)
        self._snmp2b.setContentsMargins(0,0,0,0)
        self._snmp2bWrite   = QLineEdit(self)
        self._snmp2bRead    = QLineEdit(self)
        self._snmp2bLay     = QFormLayout(self._snmp2b)
        self._snmp2b.setLayout(self._snmp2bLay)
        self._snmp2bLay.insertRow(0, 'Read community',  self._snmp2bRead)
        self._snmp2bLay.insertRow(1, 'Write community', self._snmp2bWrite)

        self._snmp3 = QGroupBox(self)
        self._snmp3.setContentsMargins(0,0,0,0)
        self._snmp3Auth     = QLineEdit(self)
        self._snmp3AuthVal  = QLineEdit(self)
        self._snmp3Priv     = QLineEdit(self)
        self._snmp3PrivVal  = QLineEdit(self)
        self._snmp3SecName  = QLineEdit(self)
        self._snmp3Lay      = QFormLayout(self._snmp3)
        self._snmp3.setLayout(self._snmp3Lay)
        self._snmp3Lay.insertRow(0, 'Auth',         self._snmp3Auth)
        self._snmp3Lay.insertRow(1, 'Auth value',   self._snmp3AuthVal)
        self._snmp3Lay.insertRow(2, 'Priv proto',   self._snmp3Priv)
        self._snmp3Lay.insertRow(3, 'Priv value',   self._snmp3PrivVal)
        self._snmp3Lay.insertRow(4, 'Sec name',     self._snmp3SecName)

        self._snmpLay = QStackedWidget(self)
        self._snmpLay.insertWidget(SNMP_V3, self._snmp3)
        self._snmpLay.insertWidget(SNMP_V2, self._snmp2b)

        self._snmpButton = QComboBox(self)
        self._snmpButton.insertItem(SNMP_V3, 'SNMP version 3')
        self._snmpButton.insertItem(SNMP_V2, 'SNMP version 2b')
        self._snmpButton.currentIndexChanged[int].connect(self._snmpLay.setCurrentIndex)
        self._snmpButton.setFocusPolicy(Qt.ClickFocus)


        # final layout
        tempLayout.addWidget(self._ipButton,                            0,0)
        tempLayout.addWidget(self._ipLine,                              0,1)
        tempLayout.addWidget(self._snmpButton,                          1,0)
        tempLayout.addWidget(self._snmpLay,                             1,1,2,1)

        tempLayout.setAlignment(self._snmpButton, Qt.AlignVCenter)
        tempLayout.setColumnStretch(0,0)
        tempLayout.setColumnStretch(1,1)
        tempLayout.setRowStretch(0,0)
        tempLayout.setRowStretch(1,0)
        tempLayout.setRowStretch(2,1)
        tempLayout.setRowStretch(3,9)
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
        return 2

    def validatePage(self):
#         snmpV2Read  = self._snmpV2Read.text()
#         snmpV2Write = self._snmpV2Write.text()
#         ipAddress   = self._ipLine.text()
# 
#         snmpVersion = self._snmpButton.currentIndex()
#         ipVersion   = self._ipButton.currentIndex()
#         print "snmp version is ", snmpVersion, " ip ", ipVersion
# 
#         perms       = (["admin"], ["admin"])
#         tpl         = "Generic SNMP element"
# 
#         if self._assertCmd(
#             snmpVersion,
#             ipVersion,
#             snmpV2Read,
#             snmpV2Write,
#             ipAddress
#         ):
#             print "true?"
#             ret = supercast.send(
#                 'monitorCreateTarget', 
#                 (
#                     ipAddress,
#                     perms,
#                     "undefined",
#                     snmpV2Read,
#                     snmpV2Write,
#                     tpl
#                 ),
#                 self.monitorReply
#             )
# 
        self.dial = WaitBox(self)
        #self.dial.setModal(True)
        #self.dial.setText(self.tr('Waiting for server response'))
        #button = self.dial.buttons()
        #self.dial.exec_()
        return False

    def _assertCmd(self, a,b,c,d,e): return True

    def monitorReply(self, msg):
        print "get reply!!!!!!", msg

class WaitBox(QProgressDialog):
    def __init__(self, parent=None):
        super(WaitBox, self).__init__(parent)

        ip_ver   = parent._snmpButton.currentIndex()
        snmp_ver = parent._ipButton.currentIndex()
        if snmp_ver == SNMP_V2:
            snmpV2Read  = parent._snmp2bRead.text()
            snmpV2Write = parent._snmp2bWrite.text()
            if ip_ver == IP_V4:
                ip4 = parent._ip4.text()
                # TODO build monitorQuerySnmpElement PDU
            else:
                ip6 = parent._ip6.text()
                # TODO build monitorQuerySnmpElement PDU

        # TODO send PDU and receive reply

        self.setMinimum(0)
        self.setMaximum(0)
        self.setLabelText('Waiting server reply')
        self.exec_()



class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setTitle(self.tr('Create a network element'))
