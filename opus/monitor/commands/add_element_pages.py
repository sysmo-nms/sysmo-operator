from PySide.QtGui   import (
    QTextEdit,
    QWizard,
    QRadioButton,
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
    QGridLayout,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView
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
import pprint

import nocapi
import opus.monitor.api as monapi
import supercast.main   as supercast

SNMP_V3  = 0
SNMP_V2  = 1
SNMP_V1  = 2

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

class Page10(QWizardPage):
    def __init__(self, parent=None):
        super(Page10, self).__init__(parent)

        self.setTitle(self.tr('Create a network element'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network element to the main configuration
        '''))
        grid = NGrid(self)
        grid.setRowStretch(1,0)
        grid.setRowStretch(10,1)
        self.setLayout(grid)

        # ipv4/6 selection and edition
        ipFormFrame = QGroupBox('IP configuration', self)
        ipForm = QFormLayout(ipFormFrame)
        ipForm.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        ipFormFrame.setLayout(ipForm)

        self._ipLabel = QLabel('Address:', self)
        self._ip4 = NIpv4Form(self)
        self._ip6 = NIpv6Form(self)
        self._ipLine = QStackedWidget(self)
        self._ipLine.insertWidget(IP_V4, self._ip4)
        self._ipLine.insertWidget(IP_V6, self._ip6)
        self._ipv4Button = QRadioButton('Version 4', self)
        self._ipv6Button = QRadioButton('Version 6', self)
        self._ipvButtonGroup = QButtonGroup(self)
        self._ipvButtonGroup.setExclusive(True)
        self._ipvButtonGroup.addButton(self._ipv4Button, IP_V4)
        self._ipvButtonGroup.addButton(self._ipv6Button, IP_V6)
        self._ipvButtonGroup.buttonPressed[int].connect(self._ipLine.setCurrentIndex)
        self._ipv4Button.setChecked(True)
        ipForm.addRow(self._ipv4Button)
        ipForm.addRow(self._ipv6Button)
        ipForm.addRow(self._ipLabel, self._ipLine)

        grid.addWidget(ipFormFrame,    0,0)

        # separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.NoFrame)
        sep2 = QFrame(self)
        sep2.setFrameShape(QFrame.NoFrame)
        grid.addWidget(sep, 1,0)
        grid.addWidget(sep2,2,0)

        # SNMP checkbox
        self._snmpCheck = QCheckBox('Is SNMP enabled', self)
        self._snmpCheck.setChecked(False)

        # SNMP sysBox
        self._snmpSysBox = QGroupBox(self)
        sysBoxLay = QFormLayout(self._snmpSysBox)

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

        # retries selection and edition
        self._retriesLabel = QLabel('Retries:', self)
        self._retries = QSpinBox(self)
        self._retries.setMinimum(0)
        self._retries.setMaximum(5)
        self._retries.setValue(1)

        # separator
        sep3 = QFrame(self)
        sep3.setFrameShape(QFrame.NoFrame)

        # version
        self._snmpButtonLabel = QLabel('Version:')
        self._snmpButton = QComboBox(self)
        self._snmpButton.insertItem(SNMP_V3, 'SNMP version 3')
        self._snmpButton.insertItem(SNMP_V2, 'SNMP version 2c')
        self._snmpButton.insertItem(SNMP_V1, 'SNMP version 1')
        self._snmpButton.setCurrentIndex(SNMP_V2)
        self._snmpButton.currentIndexChanged[int].connect(self._snmpVerClic)


        sysBoxLay.addRow(self._portLabel, self._port)
        sysBoxLay.addRow(self._timeoutLabel, self._timeout)
        sysBoxLay.addRow(self._retriesLabel, self._retries)
        sysBoxLay.addRow(sep3)
        sysBoxLay.addRow(self._snmpButtonLabel, self._snmpButton)
        sysBoxLay.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self._snmpSysBox.setDisabled(True)


        # SNMP confBox
        self._snmpBox    = NFrameContainer(self)
        self._snmpBox.setEnabled(False)
        self._snmpLayout = NGridContainer(self._snmpBox)
        self._snmpLayout.setColumnStretch(0,0)
        self._snmpLayout.setColumnStretch(1,1)


        self._snmpCheck.clicked[bool].connect(self._snmpBox.setEnabled)
        self._snmpCheck.clicked[bool].connect(self._snmpSysBox.setEnabled)
        grid.addWidget(self._snmpCheck, 3,0)
        grid.addWidget(self._snmpSysBox, 4,0)
        grid.addWidget(self._snmpBox, 5,0)


        self._snmpCom = QGroupBox('Version 1/2c specific', self)
        self._snmpComLay = NGrid(self._snmpCom)
        self._snmpComLay.addWidget(QLabel('Community:', self), 0,0)
        self._snmpComLay.addWidget(QLineEdit(self), 0,1)
        self._snmpComLay.setRowStretch(0,0)
        self._snmpComLay.setRowStretch(1,1)
        self._snmpLayout.addWidget(self._snmpCom, 3,0)

        # snmpv3 form
        self._snmp3 = QGroupBox('Version 3 specific', self)
        self._snmp3.setDisabled(True)
        self._snmp3User = QLineEdit(self)
        self._snmpLayout.addWidget(self._snmp3,3,1)


        
        self._snmp3SecLevel = QComboBox(self)
        self._snmp3SecLevel.insertItem(AUTH_PRIV, 'authPriv')
        self._snmp3SecLevel.insertItem(AUTH_NO_PRIV, 'authNoPriv')
        self._snmp3SecLevel.insertItem(NO_AUTH_NO_PRIV, 'noAuthNoPriv')
        self._snmp3SecLevel.currentIndexChanged[int].connect(self._setSecLevel)
        auth = QComboBox(self)
        auth.insertItem(AUTH_SHA,  'SHA')
        auth.insertItem(AUTH_MD5,  'MD5')
        auth.setCurrentIndex(AUTH_MD5)
        self._snmp3AuthLab  = QLabel('Authentication:', self)
        self._snmp3Auth     = auth
        self._snmp3Auth.setFixedWidth(100)
        self._snmp3AuthVal  = QLineEdit(self)
        self._snmp3AuthVal.setEchoMode(QLineEdit.Password)
        self._snmp3AuthVal.setPlaceholderText('Auth key')
        priv = QComboBox(self)
        priv.insertItem(PRIV_AES128, 'AES (128)')
        priv.insertItem(PRIV_DES,    'DES')
        priv.insertSeparator(2)  
        priv.insertItem(PRIV_AES192, 'AES 192')
        priv.insertItem(PRIV_AES256, 'AES 256')
        priv.insertItem(PRIV_3DES,   '3DES')
        priv.setCurrentIndex(PRIV_DES)
        self._snmp3PrivLab  = QLabel('Privacy:', self)
        self._snmp3Priv     = priv
        self._snmp3Priv.setFixedWidth(100)
        self._snmp3PrivVal  = QLineEdit(self)
        self._snmp3PrivVal.setEchoMode(QLineEdit.Password)
        self._snmp3PrivVal.setPlaceholderText('Priv key')

        self._snmp3SecLevel.setCurrentIndex(AUTH_PRIV)

        self._snmp3Lay      = QFormLayout(self._snmp3)
        self._snmp3Lay.setVerticalSpacing(8)
        self._snmp3Lay.setContentsMargins(15,10,15,10)
        self._snmp3.setLayout(self._snmp3Lay)

        authFrame = NFrameContainer(self)
        authFrameLay = NGridContainer(authFrame)
        authFrameLay.addWidget(self._snmp3Auth,    0,0)
        authFrameLay.addWidget(self._snmp3AuthVal, 0,1)
        self._authShowCheck = QCheckBox('show', self)
        self._authShowCheck.stateChanged.connect(self._toggleShowAuth)
        authFrameLay.addWidget(self._authShowCheck,  0,2)
        authFrameLay.setColumnStretch(0,0)
        authFrameLay.setColumnStretch(1,1)
        authFrameLay.setHorizontalSpacing(3)


        privFrame = NFrameContainer(self)
        privFrameLay = NGridContainer(privFrame)
        privFrameLay.addWidget(self._snmp3Priv,    0,0)
        privFrameLay.addWidget(self._snmp3PrivVal, 0,1)
        self._privShowCheck = QCheckBox('show', self)
        self._privShowCheck.stateChanged.connect(self._toggleShowPriv)
        privFrameLay.addWidget(self._privShowCheck,  0,2)
        privFrameLay.setColumnStretch(0,0)
        privFrameLay.setColumnStretch(1,1)
        privFrameLay.setHorizontalSpacing(3)

        self._setSecLevel(AUTH_PRIV)

        self._snmp3Lay.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self._snmp3Lay.addRow(QLabel('Security level:'),   self._snmp3SecLevel)
        #self._snmp3Lay.addWidget(self._snmp3SecLevel,         2,1,1,2)
        self._snmp3Lay.addRow(QLabel('User name:'), self._snmp3User)
        #self._snmp3Lay.addWidget(self._snmp3User,             4,1,1,2)
        self._snmp3Lay.addRow(self._snmp3AuthLab, authFrame)
        #self._snmp3Lay.addWidget(seclFrame,                   5,1,2,2)
        #self._snmp3Lay.addWidget(self._snmp3Auth,             5,1)
        #self._snmp3Lay.addWidget(self._snmp3AuthVal,          5,3)
        self._snmp3Lay.addRow(self._snmp3PrivLab,         privFrame)
        #self._snmp3Lay.addWidget(self._snmp3Priv,             6,1)
        #self._snmp3Lay.addWidget(self._snmp3PrivVal,          6,3)

        #self._snmp3Lay.setRowStretch(1,0)
        #self._snmp3Lay.setRowStretch(2,0)
        #self._snmp3Lay.setRowStretch(3,0)
        #self._snmp3Lay.setRowStretch(4,0)
        #self._snmp3Lay.setRowStretch(5,0)
        #self._snmp3Lay.setRowStretch(6,0)
        #self._snmp3Lay.setRowStretch(7,0)
        #self._snmp3Lay.setRowStretch(10,1)


# 
#         # port selection and edition
#         self._portLabel = QLabel('Port:', self)
#         self._port = QSpinBox(self)
#         self._port.setMinimum(1)
#         self._port.setMaximum(65535)
#         self._port.setValue(161)
#         form.addRow(self._portLabel, self._port)
# 
#         # timeout selection and edition
#         self._timeoutLabel = QLabel('Timeout:', self)
#         self._timeout = QSpinBox(self)
#         self._timeout.setToolTip('Snmp timeout in milliseconds')
#         self._timeout.setMinimum(100)
#         self._timeout.setMaximum(20000)
#         self._timeout.setSuffix('ms')
#         self._timeout.setValue(2500)
#         form.addRow(self._timeoutLabel, self._timeout)
# 
#         # retries selection and edition
#         self._retriesLabel = QLabel('Retries:', self)
#         self._retries = QSpinBox(self)
#         self._retries.setToolTip('If SNMP request fail, try again N times')
#         self._retries.setMinimum(0)
#         self._retries.setMaximum(5)
#         self._retries.setValue(1)
#         form.addRow(self._retriesLabel, self._retries)
# 
#         # SNMP version
#         #self._snmpVersionLabel = QLabel('SNMP version:', self)
#         #self._snmpVersion = QComboBox(self)
#         #self._snmpVersion.insertItem(SNMP_V3, 'SNMP version 3')
#         #self._snmpVersion.insertItem(SNMP_V2, 'SNMP version 2c')
#         #self._snmpVersion.insertItem(SNMP_V1, 'SNMP version 1')
#         #self._snmpVersion.currentIndexChanged[int].connect(self._snmpLay.setCurrentIndex)
#         #self._snmpVersion.setFocusPolicy(Qt.ClickFocus)
#         #form.addRow(self._snmpVersion, QLineEdit(self))
#         self._snmpPermsLabel = QLabel('Permissions:', self)
#         self._snmpPerms = QTextEdit(self)
#         form.addRow(self._snmpPermsLabel, self._snmpPerms)
# 
#         self._setDisableSNMP()
#     
#     def _setDisableSNMP(self):
#         self._timeoutLabel.setDisabled(True)
#         self._timeout.setDisabled(True)
#         self._portLabel.setDisabled(True)
#         self._port.setDisabled(True)
#         self._retriesLabel.setDisabled(True)
#         self._retries.setDisabled(True)
#         self._snmpPermsLabel.setDisabled(True)
#         self._snmpPerms.setDisabled(True)


    def _toggleShowPriv(self):
        if self._snmp3PrivVal.echoMode() == QLineEdit.Normal:
            self._snmp3PrivVal.setEchoMode(QLineEdit.Password)
        else:
            self._snmp3PrivVal.setEchoMode(QLineEdit.Normal)

    def _toggleShowAuth(self):
        if self._snmp3AuthVal.echoMode() == QLineEdit.Normal:
            self._snmp3AuthVal.setEchoMode(QLineEdit.Password)
        else:
            self._snmp3AuthVal.setEchoMode(QLineEdit.Normal)


    def nextId(self):
        return 20

    def _snmpVerClic(self, index):
        if index == SNMP_V3:
            self._snmpCom.setDisabled(True)
            self._snmp3.setDisabled(False)
        else:
            self._snmpCom.setDisabled(False)
            self._snmp3.setDisabled(True)

    def _setSecLevel(self, index):
        if index == NO_AUTH_NO_PRIV:
            self._snmp3Auth.setDisabled(True)
            self._snmp3AuthVal.setDisabled(True)
            self._snmp3AuthLab.setDisabled(True)
            self._snmp3Priv.setDisabled(True)
            self._snmp3PrivVal.setDisabled(True)
            self._snmp3PrivLab.setDisabled(True)
            self._authShowCheck.setDisabled(True)
            self._privShowCheck.setDisabled(True)
        if index == AUTH_NO_PRIV:
            self._snmp3Auth.setDisabled(False)
            self._snmp3AuthVal.setDisabled(False)
            self._snmp3AuthLab.setDisabled(False)
            self._snmp3Priv.setDisabled(True)
            self._snmp3PrivVal.setDisabled(True)
            self._snmp3PrivLab.setDisabled(True)
            self._authShowCheck.setDisabled(False)
            self._privShowCheck.setDisabled(True)
        if index == AUTH_PRIV:
            self._snmp3Auth.setDisabled(False)
            self._snmp3AuthVal.setDisabled(False)
            self._snmp3AuthLab.setDisabled(False)
            self._snmp3Priv.setDisabled(False)
            self._snmp3PrivVal.setDisabled(False)
            self._snmp3PrivLab.setDisabled(False)
            self._authShowCheck.setDisabled(False)
            self._privShowCheck.setDisabled(False)



class Page20(QWizardPage):
    def __init__(self, parent=None):
        super(Page20, self).__init__(parent)
        self.setTitle(self.tr('Create a network element'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network element to the main configuration
        '''))
        
    def nextId(self):
        return 30


class Page30(QWizardPage):
    def __init__(self, parent=None):
        super(Page30, self).__init__(parent)
        self.setTitle(self.tr('Create a network element'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network element to the main configuration
        '''))

    def nextId(self):
        return -1

class Page1(QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self._wizard = parent
        self._snmpCommandComplete = False
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
        self._ipButton.setCurrentIndex(IP_V4)
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

        # snmpv1 form
        self._snmp1Community   = QLineEdit(self)
        self._snmp1Community.setPlaceholderText("Community string")
        self._snmp1    = NFrameContainer(self)
        self._snmp1Lay = NGridContainer(self._snmp1)
        self._snmp1Lay.setRowStretch(0,0)
        self._snmp1Lay.setRowStretch(1,1)
        self._snmp1Lay.addWidget(self._snmp1Community,     0,0)

        # snmpv2 form
        self._snmp2Community   = QLineEdit(self)
        self._snmp2Community.setPlaceholderText("Community string")
        self._snmp2    = NFrameContainer(self)
        self._snmp2Lay = NGridContainer(self._snmp2)
        self._snmp2Lay.setRowStretch(0,0)
        self._snmp2Lay.setRowStretch(1,1)
        self._snmp2Lay.addWidget(self._snmp2Community,     0,0)

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


        # snmpv1/2/3 stacked layout
        self._snmpLay = QStackedWidget(self)
        self._snmpLay.insertWidget(SNMP_V3, self._snmp3)
        self._snmpLay.insertWidget(SNMP_V2, self._snmp2)
        self._snmpLay.insertWidget(SNMP_V1, self._snmp1)

        self._snmpButton = QComboBox(self)
        self._snmpButton.insertItem(SNMP_V3, 'SNMP version 3')
        self._snmpButton.insertItem(SNMP_V2, 'SNMP version 2c')
        self._snmpButton.insertItem(SNMP_V1, 'SNMP version 1')
        self._snmpButton.currentIndexChanged[int].connect(self._snmpLay.setCurrentIndex)
        self._snmpButton.setFocusPolicy(Qt.ClickFocus)

        # register fields
        self.registerField('ip_version',        self._ipButton)
        self.registerField('ip6_value',         self._ip6)
        self.registerField('ip4_value',         self._ip4)
        self.registerField('ip_port',           self._port)
        self.registerField('snmp_timeout',      self._timeout)
        self.registerField('snmp_version',      self._snmpButton)
        self.registerField('snmp_v1_community', self._snmp1Community)
        self.registerField('snmp_v2_community', self._snmp2Community)
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
        self._snmp1Community.textChanged.connect(self._updateComplete)
        self._snmp2Community.textChanged.connect(self._updateComplete)
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

        self._forTest()
    

    # VALIDATION SYSTEM
    def _updateComplete(self, _):
        self._snmpCommandComplete = False
        self.completeChanged.emit()

    def isComplete(self):
        # ip is complete?
        if self.field('ip_version') == IP_V4:
            if self._ip4.hasAcceptableInput() != True: return False
        else:
            if self._ip6.hasAcceptableInput() != True: return False

        # snmp is complete?
        snmpver = self.field('snmp_version')
        if  snmpver == SNMP_V1:
            community = self.field('snmp_v1_community')
            if community == "": return False
        if  snmpver == SNMP_V2:
            community = self.field('snmp_v2_community')
            if community == "": return False
        else:
            user = self.field('snmp_v3_user')
            auth = self.field('snmp_v3_auth_val')
            priv = self.field('snmp_v3_priv_val')
            if user == "": return False
            if self.field('snmp_v3_sec_level') == AUTH_NO_PRIV:
                if auth == "": return False
            if self.field('snmp_v3_sec_level') == AUTH_PRIV:
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

    def _forTest(self):
        self._ip4.setText("192.168.0.5")
        self._snmp2Community.setText("public")
        self._snmpButton.setCurrentIndex(SNMP_V2)

    def nextId(self):
        return 2

    def validatePage(self):
        if self._snmpCommandComplete == False:
            self.dial = WaitSnmpInfoBox(self)
            return False
        else:
            return True


    def setSysInfo(self, info):
        self._wizard.setSysInfo(info)

    def setIfInfo(self, info):
        self._wizard.setIfInfo(info)

    def setEngineId(self, info):
        self._wizard.setEngineId(info)

    def triggerValidate(self):
        self._snmpCommandComplete = True
        self._wizard.next()

class WaitSnmpInfoBox(QProgressDialog):
    def __init__(self, parent=None):
        super(WaitSnmpInfoBox, self).__init__(parent)

        self._wizPage = parent
        self._elementName        = ""
        self._elementEgineId     = ""
        self._elementInterfaces  = ""

        self.setMinimum(0)
        self.setMaximum(4)
        self.setValue(0)
        self.setLabelText('Acquire lock...')

        self.setModal(True)
        self.show()
        self._executeInfo()

    def _executeInfo(self):
        ipv = self._wizPage.field('ip_version')
        if ipv == IP_V4:
            ipv = "v4"
            ip  = self._wizPage.field('ip4_value')
        else:
            ipv = "v6"
            ip  = self._wizPage.field('ip6_value')

        port    = self._wizPage.field('ip_port')
        timeout = self._wizPage.field('snmp_timeout')
        snmpVer = self._wizPage.field('snmp_version')
        if snmpVer == SNMP_V1:
            community = self._wizPage.field('snmp_v1_community')
            snmpVer     = "1"
            v3SecL      = "noAuthNoPriv"
            v3User      = "undefined"
            v3AuthAlg   = "SHA"
            v3AuthKey   = "undefined"
            v3PrivAlg   = "AES"
            v3PrivKey   = "undefined"
        if snmpVer == SNMP_V2:
            community   = self._wizPage.field('snmp_v2_community')
            snmpVer     = "2c"
            v3SecL      = "noAuthNoPriv"
            v3User      = "undefined"
            v3AuthAlg   = "SHA"
            v3AuthKey   = "undefined"
            v3PrivAlg   = "AES"
            v3PrivKey   = "undefined"
        else:
            v3SecLevel  = self._wizPage.field('snmp_v3_sec_level')
            v3User      = self._wizPage.field('snmp_v3_user')
            community   = "undefined"
            snmpVer     = "3"
            if v3SecLevel == NO_AUTH_NO_PRIV:
                v3SecL      = 'noAuthNoPriv'
                v3AuthKey   = "undefined"
                v3PrivKey   = "undefined"
            elif v3SecLevel == AUTH_NO_PRIV:
                v3SecL      = 'authNoPriv'
                v3AuthKey   = self._wizPage.field('snmp_v3_auth_val')
                v3PrivKey   = "undefined"
            elif v3SecLevel == AUTH_PRIV:
                v3SecL      = 'authPriv'
                v3AuthKey   = self._wizPage.field('snmp_v3_auth_val')
                v3PrivKey   = self._wizPage.field('snmp_v3_priv_val')

            v3AuthAlgo = self._wizPage.field('snmp_v3_auth_alg')
            if v3AuthAlgo == AUTH_SHA:
                v3AuthAlg = 'SHA'
            elif v3AuthAlgo == AUTH_MD5:
                v3AuthAlg = 'MD5'

            v3PrivAlgo = self._wizPage.field('snmp_v3_priv_alg')
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

        supercast.send(
            'monitorSnmpElementInfoQuery',
            (
                ipv,
                ip,
                port,
                timeout,
                snmpVer,
                community,
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
        if reply['value']['status'] == False:
            err = QMessageBox(self)
            err.setModal(True)
            err.setIconPixmap(nocapi.nGetPixmap('dialog-information'))
            err.setText("Snmp manager failed to get information for element:")
            err.setInformativeText("ERROR: " + reply['value']['reply'])
            err.finished[int].connect(self._closeMe)
            err.open()
            return

        self.setValue(self.value() + 1)

        if (self.value() == 1):
            self.setLabelText("Get engine ID...")
        elif (self.value() == 2):
            self._elementName   = reply['value']['reply']
            self.setLabelText("Get interfaces infos...")
        elif (self.value() == 3):
            self._elementInterfaces = reply['value']['reply']


        if reply['value']['replyType'] == 'snmpSystemInfo':
            self._wizPage.setSysInfo(reply['value']['reply'])
        elif reply['value']['replyType'] == 'snmpInterfacesInfo':
            self._wizPage.setIfInfo(reply['value']['reply'])

        if reply['lastPdu'] == True:
            if reply['value']['status'] == True:
                self._wizPage.triggerValidate()
            self.deleteLater()
            return
        
    def _closeMe(self, a):
        self.deleteLater()


class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self._wizard = parent
        self.setTitle(self.tr('Configure element properties'))
        self.setSubTitle(self.tr('''
            Chose interfaces to monitor on the device
        '''))
    
        self._grid = NGrid(self)
        self.setLayout(self._grid)

        infoFrame = NFrame(self)
        infoLayout = NGridContainer(infoFrame)
        infoLayout.addWidget(QLabel("Tips blablab al", infoFrame), 0,0)

        ifFrame = NFrame(self)
        ifLayout = NGridContainer(ifFrame)
        ifFrame.setLayout(ifLayout)
        self._treeWidget = QTreeWidget(ifFrame)
        self._treeWidget.setColumnCount(5)
        self._treeWidget.setHeaderLabels([
            'Descr', 'Admin status', 'Oper status', 
            'Physical address', 'Type'])
        self._treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        ifLayout.addWidget(self._treeWidget)

        self._grid.addWidget(infoFrame,  0,0)
        self._grid.addWidget(ifFrame,    1,0)

    def validatePage(self):
        count = self._treeWidget.topLevelItemCount()
        selectedIfs = list()
        for index in range(count):
            item = self._treeWidget.topLevelItem(index)
            if (item.checkState(0) == Qt.CheckState.Checked):
                selectedIfs.append(int(item.text(5)))

        self._wizard.setIfSelection(selectedIfs)
        return True

    def nextId(self):
        return 3

    def initializePage(self):
        self._treeWidget.clear()
        ifInfos = self._wizard._ifInfo
        for ifDef in ifInfos:
            ifSpeed = ifDef['ifSpeed']
            ifType  = ifDef['ifType']
            ifLastChange = ifDef['ifLastChange']
            ifPhysaddress = ifDef['ifPhysaddress']
            ifAdminStatus = ifDef['ifAdminStatus']
            ifDescr = ifDef['ifDescr']
            ifIndex = ifDef['ifIndex']
            ifMTU   = ifDef['ifMTU']
            ifOperStatus = ifDef['ifOperStatus']
            item = QTreeWidgetItem()
            item.setText(0, ifDescr)
            item.setText(1, str(ifAdminStatus))
            item.setText(2, str(ifOperStatus))
            item.setText(3, ifPhysaddress)
            item.setText(4, str(ifType))
            item.setText(5, str(ifIndex))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
            self._treeWidget.addTopLevelItem(item)




class Page3(QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self._wizard = parent
        self.setTitle(self.tr('Final step'))
        self.setSubTitle(self.tr('''
            Validate the following configuration
        '''))
        self._grid = NGridContainer(self)
        self.setLayout(self._grid)

    def validatePage(self):
        self.dial = WaitRegisterElementBox(self)
        print "validate"
        return False

    def nextId(self):
        print "next id here?"
        return -1

    def initializePage(self):
        eConf = dict()
        eConf['ip_version'] = self.field('ip_version')
        eConf['ip6_value'] = self.field('ip6_value')
        eConf['ip4_value'] = self.field('ip4_value')
        eConf['ip_port'] = self.field('ip_port')
        eConf['snmp_timeout'] = self.field('snmp_timeout')
        eConf['snmp_version'] = self.field('snmp_version')
        eConf['snmp_v1_community'] = self.field('snmp_v1_community')
        eConf['snmp_v2_community'] = self.field('snmp_v2_community')
        eConf['snmp_v3_user'] = self.field('snmp_v3_user')
        eConf['snmp_v3_sec_level'] = self.field('snmp_v3_sec_level')
        eConf['snmp_v3_auth_alg'] = self.field('snmp_v3_auth_alg')
        eConf['snmp_v3_auth_val'] = self.field('snmp_v3_auth_val')
        eConf['snmp_v3_priv_alg'] = self.field('snmp_v3_priv_alg')
        eConf['snmp_v3_priv_val'] = self.field('snmp_v3_priv_val')
        eConf['if_selection']  = self._wizard._ifSelection
        i = 0
        for key in eConf.keys():
            st = "%s %s" % (key, eConf[key])
            lab = QLabel(st, self)
            self._grid.addWidget(lab, i,0)
            i += 1
        

class WaitRegisterElementBox(QProgressDialog):
    def __init__(self, parent=None):
        super(WaitRegisterElementBox, self).__init__(parent)
        self._wizPage = parent
        self.setMinimum(0)
        self.setMaximum(4)
        self.setValue(0)
        self.setLabelText('Acquire lock...')
        self.setModal(True)
        self.show()
        self._executeInfo()

    def _executeInfo(self):
        ipvf = self._wizPage.field('ip_version')
        if ipvf == IP_V4:
            ipv = "v4"
            ip  = self._wizPage.field('ip4_value')
        else:
            ipv = "v6"
            ip  = self._wizPage.field('ip6_value')

        port    = self._wizPage.field('ip_port')
        timeout = self._wizPage.field('snmp_timeout')
        snmpVer = self._wizPage.field('snmp_version')
        if snmpVer == SNMP_V1:
            community = self._wizPage.field('snmp_v1_community')
            snmpVer = "1"
            v3SecL  = "noAuthNoPriv"
            v3User  = "undefined"
            v3AuthAlg = "SHA"
            v3AuthKey = "undefined"
            v3PrivAlg = "AES"
            v3PrivKey = "undefined"
        if snmpVer == SNMP_V2:
            community = self._wizPage.field('snmp_v2_community')
            snmpVer = "2c"
            v3SecL  = "noAuthNoPriv"
            v3User  = "undefined"
            v3AuthAlg = "SHA"
            v3AuthKey = "undefined"
            v3PrivAlg = "AES"
            v3PrivKey = "undefined"
        else:
            v3User  =   self._wizPage.field('snmp_v3_user')
            v3SecLevel = self._wizPage.field('snmp_v3_sec_level')
            if v3SecLevel == NO_AUTH_NO_PRIV:
                v3SecL = 'noAuthNoPriv'
                v3AuthKey = "undefined"
                v3PrivKey = "undefined"
            elif v3SecLevel == AUTH_NO_PRIV:
                v3SecL = 'authNoPriv'
                v3AuthKey = self._wizPage.field('snmp_v3_auth_val')
                v3PrivKey = "undefined"
            elif v3SecLevel == AUTH_PRIV:
                v3SecL = 'authPriv'
                v3AuthKey = self._wizPage.field('snmp_v3_auth_val')
                v3PrivKey = self._wizPage.field('snmp_v3_priv_val')

            v3AuthAlgo = self._wizPage.field('snmp_v3_auth_alg')
            if v3AuthAlgo == AUTH_SHA:
                v3AuthAlg = 'SHA'
            elif v3AuthAlgo == AUTH_MD5:
                v3AuthAlg = 'MD5'

            v3PrivAlgo = self._wizPage.field('snmp_v3_priv_alg')
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

            community = "undefined"
            snmpVer = "3"

        ifSelection = self._wizPage._wizard._ifSelection

        print "if selection: ", ifSelection
        supercast.send(
            'monitorSnmpElementCreateQuery',
            (
                ipv,
                ip,
                port,
                timeout,
                snmpVer,
                community,
                v3SecL,
                v3User,
                v3AuthAlg,
                v3AuthKey,
                v3PrivAlg,
                v3PrivKey,
                ifSelection
            ),
            self._elementInfoReply
        )

    def _elementInfoReply(self, value):
        trayicon = nocapi.nGetSystemTrayIcon()
        trayicon.showMessage('Create SNMP element return:', 'Sucess', msecs=3000)
        self.deleteLater()
