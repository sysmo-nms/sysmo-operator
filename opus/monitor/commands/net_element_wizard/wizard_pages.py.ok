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

AUTH_SHA  = 0
AUTH_MD5  = 1

PRIV_AES128 = 0
PRIV_DES    = 1
PRIV_AES192 = 3
PRIV_AES256 = 4
PRIV_3DES   = 5

AUTH_PRIV       = 0
AUTH_NO_PRIV    = 1
NO_AUTH_NO_PRIV = 2

IP_V4    = 0
IP_V6    = 1

class Page1(QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self._wizard = parent
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
        self._snmp2b.setContentsMargins(15,15,15,15)
        self._snmp2bRw   = QLineEdit(self)
        self._snmp2bRo    = QLineEdit(self)
        self._snmp2bLay     = QFormLayout(self._snmp2b)
        self._snmp2bLay.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self._snmp2b.setLayout(self._snmp2bLay)
        self._snmp2bLay.insertRow(1, 'Read only community',  self._snmp2bRo)
        self._snmp2bLay.insertRow(2, 'Read/write community', self._snmp2bRw)


        # snmpv3 form
        self._snmp3 = QGroupBox(self)
        self._snmp3User = QLineEdit(self)
        self._snmp3SecLevel = QComboBox(self)
        self._snmp3SecLevel.insertItem(AUTH_PRIV, 'authPriv')
        self._snmp3SecLevel.insertItem(AUTH_NO_PRIV, 'authNoPriv')
        self._snmp3SecLevel.insertItem(NO_AUTH_NO_PRIV, 'noAuthNoPriv')
        self._snmp3SecLevel.currentIndexChanged[int].connect(self._setSecLevel)
        auth = QComboBox(self)
        auth.insertItem(AUTH_SHA,  'SHA')
        auth.insertItem(AUTH_MD5,  'MD5')
        self._snmp3AuthLab  = QLabel('Auth algorithm:', self)
        self._snmp3Auth     = auth
        self._snmp3AuthValLab  = QLabel('Auth key:', self)
        self._snmp3AuthVal  = QLineEdit(self)
        priv = QComboBox(self)
        priv.insertItem(PRIV_AES128, 'AES (128)')
        priv.insertItem(PRIV_DES,    'DES')
        priv.insertSeparator(2)  
        priv.insertItem(PRIV_AES192, 'AES 192')
        priv.insertItem(PRIV_AES256, 'AES 256')
        priv.insertItem(PRIV_3DES,   '3DES')
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
        self.registerField('snmp_v2_ro',      self._snmp2bRo)
        self.registerField('snmp_v2_rw',     self._snmp2bRw)
        self.registerField('snmp_v3_user',      self._snmp3User)
        self.registerField('snmp_v3_sec_level', self._snmp3SecLevel)
        self.registerField('snmp_v3_auth_alg',  self._snmp3Auth)
        self.registerField('snmp_v3_auth_val',  self._snmp3AuthVal)
        self.registerField('snmp_v3_priv_alg',  self._snmp3Priv)
        self.registerField('snmp_v3_priv_val',  self._snmp3PrivVal)

        # update complete
        self._ipButton.currentIndexChanged[int].connect(self._updateComplete)
        self._ip6.textChanged.connect(self._updateComplete)
        self._ip4.textChanged.connect(self._updateComplete)
        self._port.valueChanged.connect(self._updateComplete)
        self._timeout.valueChanged.connect(self._updateComplete)
        self._snmpButton.currentIndexChanged[int].connect(self._updateComplete)
        self._snmp2bRo.textChanged.connect(self._updateComplete)
        self._snmp2bRw.textChanged.connect(self._updateComplete)
        self._snmp3SecLevel.currentIndexChanged[int].connect(self._updateComplete)
        self._snmp3AuthVal.textChanged.connect(self._updateComplete)
        self._snmp3PrivVal.textChanged.connect(self._updateComplete)

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

    # VALIDATION SYSTEM
    def _updateComplete(self, _):
        self.completeChanged.emit()

    def isComplete(self):
        # ip is complete?
        if self._wizard.field('ip_version') == IP_V4:
            if self._ip4.hasAcceptableInput() != True: return False
        else:
            if self._ip6.hasAcceptableInput() != True: return False

        # snmp is complete?
        if self._wizard.field('snmp_version') == SNMP_V2:
            read    = self._wizard.field('snmp_v2_ro')
            write   = self._wizard.field('snmp_v2_rw')
            if read == "" or write == "": return False
        else:
            user = self._wizard.field('snmp_v3_user')
            auth = self._wizard.field('snmp_v3_auth_val')
            priv = self._wizard.field('snmp_v3_priv_val')
            if user == "": return False
            if self._wizard.field('snmp_v3_sec_level') == AUTH_NO_PRIV:
                if auth == "": return False
            if self._wizard.field('snmp_v3_sec_level') == AUTH_PRIV:
                if auth == "" or priv == "": return False


        return True

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
        self.dial = WaitSnmpInfoBox(self)
        return False

class WaitSnmpInfoBox(QProgressDialog):
    def __init__(self, parent=None):
        super(WaitSnmpInfoBox, self).__init__(parent)
        self._wizard = parent._wizard
        self.setMinimum(0)
        self.setMaximum(0)
        self.setLabelText('Probing element...')

        self._executeInfo()
        self.setModal(True)
        self.show()

    def _executeInfo(self):
        ipv = self._wizard.field('ip_version')
        if ipv == IP_V4:
            ipv = 4
            ip  = self._wizard.field('ip4_value')
        else:
            ipv = 6
            ip  = self._wizard.field('ip6_value')

        port    = self._wizard.field('ip_port')
        timeout = self._wizard.field('snmp_timeout')
        snmpVer = self._wizard.field('snmp_version')
        if snmpVer == SNMP_V2:
            snmpV2Ro = self._wizard.field('snmp_v2_ro')
            snmpV2Rw = self._wizard.field('snmp_v2_rw')
            snmpVer = 2
            v3SecL  = ""
            v3User  = ""
            v3AuthAlg = ""
            v3AuthKey = ""
            v3PrivAlg = ""
            v3PrivKey = ""
        else:
            v3SecLevel = self._wizard.field('snmp_v3_sec_level')
            if v3SecLevel == NO_AUTH_NO_PRIV:
                v3SecL = 'noAuthNoPriv'
            elif v3SecLevel == AUTH_NO_PRIV:
                v3SecL = 'authNoPriv'
            elif v3SecLevel == AUTH_PRIV:
                v3SecL = 'authPriv'

            v3AuthAlgo = self._wizard.field('snmp_v3_auth_alg')
            if v3AuthAlgo == AUTH_SHA:
                v3AuthAlg = 'SHA'
            elif v3AuthAlgo == AUTH_MD5:
                v3AuthAlg = 'MD5'

            v3PrivAlgo = self._wizard.field('snmp_v3_priv_alg')
            if v3PrivAlgo == PRIV_AES128:
                v3PrivAlg = 'AES'
            elif v3PrivAlgo == PRIV_AES192:
                v3PrivAlg = 'AES192'
            elif v3PrivAlgo == PRIV_AES256:
                v3PrivAlg = 'AES256'
            elif v3PrivAlgo == PRIV_DES:
                v3PrivAlg = 'DES'
            elif v3PrivAlgo == PRIV_3DES:
                v3PrivAlg = '3DES'

            snmpV2Ro = ""
            snmpV2Rw = ""
            snmpVer = 3
            v3User  = self._wizard.field('snmp_v3_user')
            v3AuthKey = self._wizard.field('snmp_v3_auth_val')
            v3PrivKey = self._wizard.field('snmp_v3_priv_val')

        supercast.send(
            'monitorSnmpElementInfoQuery',
            (
                ipv,
                ip,
                port,
                timeout,
                snmpVer,
                snmpV2Ro,
                snmpV2Rw,
                v3SecL,
                v3User,
                v3AuthAlg,
                v3AuthKey,
                v3PrivAlg,
                v3PrivKey
            ),
            self._elementInfoReply
        )

    def _elementInfoReply(self, reply):
        print "reply!"




class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setTitle(self.tr('Select the interfaces you want to monitor'))
