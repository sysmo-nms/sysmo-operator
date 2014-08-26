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
    QProgressBar,
    QSpinBox,
    QFrame,
    QGridLayout
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

AUTH_SHA1 = 0
AUTH_MD5  = 1

PRIV_AES    = 0
PRIV_DES    = 1

AUTH_PRIV       = 0
AUTH_NO_PRIV    = 1
NO_AUTH_NO_PRIV = 2

IP_V4    = 0
IP_V6    = 1

class Page1(QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('Create a network element'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network element to the main configuration
        '''))

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


        # port selection and edition
        self._portLabel = QLabel('Port:', self)
        self._port = QSpinBox(self)
        self._port.setMinimum(1)
        self._port.setMaximum(65535)
        self._port.setValue(161)

        # timeout selection and edition
        self._timeoutLabel = QLabel('Timeout:', self)
        self._timeout = QSpinBox(self)
        self._timeout.setToolTip('Snmp timeout in milliseconds')
        self._timeout.setMinimum(100)
        self._timeout.setMaximum(20000)
        self._timeout.setValue(2500)

        # snmpv2 form
        self._snmp2b = QGroupBox(self)
        self._snmp2b.setContentsMargins(0,0,0,0)
        self._snmp2bWrite   = QLineEdit(self)
        self._snmp2bRead    = QLineEdit(self)
        self._snmp2bLay     = QFormLayout(self._snmp2b)
        self._snmp2b.setLayout(self._snmp2bLay)
        self._snmp2bLay.insertRow(0, 'Read community',  self._snmp2bRead)
        self._snmp2bLay.insertRow(1, 'Write community', self._snmp2bWrite)


        # snmpv3 form
        self._snmp3 = QGroupBox(self)
        self._snmp3User = QLineEdit(self)
        self._snmp3SecLevel = QComboBox(self)
        self._snmp3SecLevel.insertItem(AUTH_PRIV, 'authPriv')
        self._snmp3SecLevel.insertItem(AUTH_NO_PRIV, 'authNoPriv')
        self._snmp3SecLevel.insertItem(NO_AUTH_NO_PRIV, 'noAuthNoPriv')
        self._snmp3SecLevel.currentIndexChanged[int].connect(self._setSecLevel)
        auth = QComboBox(self)
        auth.insertItem(AUTH_SHA1, 'SHA1')
        auth.insertItem(AUTH_MD5,  'MD5')
        self._snmp3AuthLab  = QLabel('Auth algorithm:', self)
        self._snmp3Auth     = auth
        self._snmp3AuthValLab  = QLabel('Auth key:', self)
        self._snmp3AuthVal  = QLineEdit(self)
        priv = QComboBox(self)
        priv.insertItem(PRIV_AES, 'AES')
        priv.insertItem(PRIV_DES, 'DES')
        self._snmp3PrivLab  = QLabel('Priv algorithm:', self)
        self._snmp3Priv     = priv
        self._snmp3PrivValLab  = QLabel('Priv key:', self)
        self._snmp3PrivVal  = QLineEdit(self)

        self._snmp3SecLevel.setCurrentIndex(AUTH_PRIV)
        self._setSecLevel(AUTH_PRIV)

        self._snmp3Lay      = QGridLayout(self._snmp3)
        self._snmp3Lay.setVerticalSpacing(8)
        self._snmp3Lay.setContentsMargins(15,10,15,10)
        self._snmp3.setLayout(self._snmp3Lay)
        sep = QFrame(self)
        sep.setFrameShape(QFrame.NoFrame)
        self._snmp3Lay.addWidget(QLabel('User name:'),  0,0)
        self._snmp3Lay.addWidget(self._snmp3User,             0,1)
        self._snmp3Lay.addWidget(QLabel('Security level:'),   0,2)
        self._snmp3Lay.addWidget(self._snmp3SecLevel,         0,3)
        self._snmp3Lay.addWidget(sep,                         1,0,1,4)
        self._snmp3Lay.addWidget(self._snmp3AuthLab,          2,0)
        self._snmp3Lay.addWidget(self._snmp3Auth,             2,1)
        self._snmp3Lay.addWidget(self._snmp3AuthValLab,       2,2)
        self._snmp3Lay.addWidget(self._snmp3AuthVal,          2,3)
        self._snmp3Lay.addWidget(self._snmp3PrivLab,          3,0)
        self._snmp3Lay.addWidget(self._snmp3Priv,             3,1)
        self._snmp3Lay.addWidget(self._snmp3PrivValLab,       3,2)
        self._snmp3Lay.addWidget(self._snmp3PrivVal,          3,3)

        self._snmp3Lay.setRowStretch(1,0)
        self._snmp3Lay.setRowStretch(2,0)
        self._snmp3Lay.setRowStretch(3,0)
        self._snmp3Lay.setRowStretch(4,0)
        self._snmp3Lay.setRowStretch(10,1)


        # snmpv2/3 stacked layout
        self._snmpLay = QStackedWidget(self)
        self._snmpLay.insertWidget(SNMP_V3, self._snmp3)
        self._snmpLay.insertWidget(SNMP_V2, self._snmp2b)

        self._snmpButton = QComboBox(self)
        self._snmpButton.insertItem(SNMP_V3, 'SNMP version 3')
        self._snmpButton.insertItem(SNMP_V2, 'SNMP version 2b')
        self._snmpButton.currentIndexChanged[int].connect(self._snmpLay.setCurrentIndex)
        self._snmpButton.setFocusPolicy(Qt.ClickFocus)

        # register fields
        self.registerField('ip_version',        self._ipButton)
        self.registerField('ip6_value',         self._ip6)
        self.registerField('ip4_value',         self._ip4)
        self.registerField('ip_port',           self._port)
        self.registerField('snmp_timeout',      self._timeout)
        self.registerField('snmp_version',      self._snmpButton)
        self.registerField('snmp_v2_read',      self._snmp2bRead)
        self.registerField('snmp_v2_write',     self._snmp2bWrite)
        self.registerField('snmp_v3_sec_level', self._snmp3SecLevel)
        self.registerField('snmp_v3_auth_alg',  self._snmp3Auth)
        self.registerField('snmp_v3_auth_val',  self._snmp3AuthVal)
        self.registerField('snmp_v3_priv_alg',  self._snmp3Priv)
        self.registerField('snmp_v3_priv_val',  self._snmp3PrivVal)

        # final layout
        grid  = NGrid(self)
        grid.setContentsMargins(10,18,10,18)
        grid.setVerticalSpacing(25)
        grid.setRowStretch(1,0)
        grid.addWidget(self._ipButton,                            0,0)
        grid.addWidget(self._ipLine,                              0,1)
        grid.addWidget(self._portLabel,                           0,2)
        grid.addWidget(self._port,                                0,3)
        grid.addWidget(self._timeoutLabel,                        0,4)
        grid.addWidget(self._timeout,                             0,5)
        grid.addWidget(self._snmpButton,                          1,0)
        grid.addWidget(self._snmpLay,                             1,1,2,5)
        grid.setAlignment(self._snmpButton, Qt.AlignVCenter)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,1)
        grid.setRowStretch(3,9)
        self.setLayout(grid)

    def _setSecLevel(self, index):
        if index == NO_AUTH_NO_PRIV:
            self._snmp3Auth.setDisabled(True)
            self._snmp3AuthVal.setDisabled(True)
            self._snmp3AuthLab.setDisabled(True)
            self._snmp3AuthValLab.setDisabled(True)
            self._snmp3Priv.setDisabled(True)
            self._snmp3PrivVal.setDisabled(True)
            self._snmp3PrivLab.setDisabled(True)
            self._snmp3PrivValLab.setDisabled(True)
        if index == AUTH_NO_PRIV:
            self._snmp3Auth.setDisabled(False)
            self._snmp3AuthVal.setDisabled(False)
            self._snmp3AuthLab.setDisabled(False)
            self._snmp3AuthValLab.setDisabled(False)
            self._snmp3Priv.setDisabled(True)
            self._snmp3PrivVal.setDisabled(True)
            self._snmp3PrivLab.setDisabled(True)
            self._snmp3PrivValLab.setDisabled(True)
        if index == AUTH_PRIV:
            self._snmp3Auth.setDisabled(False)
            self._snmp3AuthVal.setDisabled(False)
            self._snmp3AuthLab.setDisabled(False)
            self._snmp3AuthValLab.setDisabled(False)
            self._snmp3Priv.setDisabled(False)
            self._snmp3PrivVal.setDisabled(False)
            self._snmp3PrivLab.setDisabled(False)
            self._snmp3PrivValLab.setDisabled(False)

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
        self.dial = WaitSnmpInfoBox(self)
        #self.dial.setModal(True)
        #self.dial.setText(self.tr('Waiting for server response'))
        #button = self.dial.buttons()
        #self.dial.exec_()
        return True

    def _assertCmd(self, a,b,c,d,e): return True

    def monitorReply(self, msg):
        print "get reply!!!!!!", msg

class WaitSnmpInfoBox(QProgressDialog):
    def __init__(self, parent=None):
        super(WaitSnmpInfoBox, self).__init__(parent)
        self.setModal(True)

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
        self.setLabelText('Probing element...')
        self.exec_()



class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setTitle(self.tr('Select the interfaces you want to monitor'))
