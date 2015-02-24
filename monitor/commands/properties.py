from PyQt5.QtWidgets   import *
from PyQt5.QtCore import Qt

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

IP_V4 = 0
IP_V6 = 1

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

class PropertiesAll(NFrame):
    def __init__(self, parent=None, conf=None):
        super(PropertiesAll, self).__init__(parent)
        grid = NGrid(self)
        self._mainConfig = MainConfigFrame(self)
        self._snmpConfig = SnmpConfigFrame(self)
        self._permConfig = PermConfigFrame(self)
        self._propConfig = PropConfigFrame(self)
        self._jobsConfig = JobsConfigFrame(self)
        self._probesConfig = ProbesConfigFrame(self)
        grid.addWidget(self._mainConfig, 0,0)
        grid.addWidget(self._snmpConfig, 0,1)
        grid.addWidget(self._permConfig, 0,2)
        grid.addWidget(self._propConfig, 1,0)
        grid.addWidget(self._jobsConfig, 1,1,1,2)
        grid.addWidget(self._probesConfig, 2,0,1,3)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,1)

class MainConfigFrame(QGroupBox):
    def __init__(self, parent=None, conf=None):
        super(MainConfigFrame, self).__init__(parent)
        self.setTitle('Main target configuration')
        form = QFormLayout(self)
        form.addRow(HelpUtil(self))

        # target name
        self._name = QLineEdit(self)
        form.addRow('Target name:', self._name)

        # ip version
        ipvFrame = NFrameContainer(self)
        ipvLay   = NGridContainer(ipvFrame)
        ipv4 = QRadioButton('Version 4', self)
        ipv6 = QRadioButton('Version 6', self)
        ipvLay.addWidget(ipv4, 0,0)
        ipvLay.addWidget(ipv6, 0,1)
        ipvLay.setColumnStretch(0,0)
        ipvLay.setColumnStretch(1,0)
        ipvLay.setColumnStretch(2,1)
        self._ipversion = QButtonGroup(self)
        self._ipversion.setExclusive(True)
        self._ipversion.addButton(ipv4, IP_V4)
        self._ipversion.addButton(ipv6, IP_V6)
        ipv4.setChecked(True)
        form.addRow('IP version:', ipvFrame)
        
        # ip line edit
        self._ip4 = NIpv4Form(self)
        self._ip6 = NIpv6Form(self)
        self._ipLineStack = QStackedWidget(self)
        self._ipLineStack.insertWidget(IP_V4, self._ip4)
        self._ipLineStack.insertWidget(IP_V6, self._ip6)
        self._ipversion.buttonPressed[int].connect(self._ipLineStack.setCurrentIndex)
        form.addRow('IP address:', self._ipLineStack)

    def isValid(self):
        if self._name.text() == "":
            return False

        if self._ipversion.checkedId() == IP_V4:
            return self._ip4.hasAcceptableInput()

        if self._ipversion.checkedId() == IP_V6:
            return self._ip6.hasAcceptableInput()

    def getConfig(self):
        vals = dict()
        if self._ipversion.checkedId() == IP_V4:
            vals['ipv'] = "4"
        else:
            vals['ipv'] = "6"
        vals['targetName'] = self._name.text()
        return vals



class SnmpConfigFrame(NFrame):
    def __init__(self, parent=None, conf=None):
        super(SnmpConfigFrame, self).__init__(parent)

        snmpEnable    = QCheckBox('SNMP enabled', self)
        snmpEnable.setChecked(False)
        snmpConfFrame = NFrameContainer(self)
        snmpConfFrame.setEnabled(False)
        snmpConfLay   = NGridContainer(snmpConfFrame)
        snmpEnable.clicked[bool].connect(snmpConfFrame.setEnabled)

        grid = NGrid(self)
        grid.addWidget(snmpEnable, 0,0)
        grid.addWidget(snmpConfFrame, 1,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)

        # version
        versionGroup = QComboBox(self)
        versionGroup.addItem('1')
        versionGroup.addItem('2c')
        versionGroup.addItem('3')
        snmpConfLay.addWidget(QLabel('Version:'), 0,0)
        snmpConfLay.addWidget(versionGroup, 0,1)

        # port selection and edition
        self._port = QSpinBox(self)
        self._port.setMinimum(1)
        self._port.setMaximum(65535)
        self._port.setValue(161)
        snmpConfLay.addWidget(QLabel('Port:', self), 0,2)
        snmpConfLay.addWidget(self._port,            0,3)

        # timeout selection and edition
        self._timeout = QSpinBox(self)
        self._timeout.setToolTip('Snmp timeout in milliseconds')
        self._timeout.setMinimum(100)
        self._timeout.setMaximum(20000)
        self._timeout.setValue(2500)
        snmpConfLay.addWidget(QLabel('Timeout:', self), 0,4)
        snmpConfLay.addWidget(self._timeout,            0,5)
        # auth

        self._snmp3 = NFrameContainer(self)
        self._snmp3.setDisabled(True)
        self._snmp3User = QLineEdit(self)
        #self._snmpLayout.addWidget(self._snmp3,3,1)
        stackConf = QStackedWidget(self)
        stackConf.insertWidget(SNMP_V3, self._snmp3)
        snmpConfLay.addWidget(stackConf, 1,0,1,6)
        snmpConfLay.setColumnStretch(0,0)
        snmpConfLay.setColumnStretch(1,0)
        snmpConfLay.setColumnStretch(2,0)
        snmpConfLay.setColumnStretch(3,0)
        snmpConfLay.setColumnStretch(4,0)
        snmpConfLay.setColumnStretch(5,1)


        
        self._snmp3SecLevel = QComboBox(self)
        self._snmp3SecLevel.insertItem(AUTH_PRIV, 'authPriv')
        self._snmp3SecLevel.insertItem(AUTH_NO_PRIV, 'authNoPriv')
        self._snmp3SecLevel.insertItem(NO_AUTH_NO_PRIV, 'noAuthNoPriv')
        #self._snmp3SecLevel.currentIndexChanged[int].connect(self._setSecLevel)
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
        #self._authShowCheck.stateChanged.connect(self._toggleShowAuth)
        authFrameLay.addWidget(self._authShowCheck,  0,2)
        authFrameLay.setColumnStretch(0,0)
        authFrameLay.setColumnStretch(1,1)
        authFrameLay.setHorizontalSpacing(3)


        privFrame = NFrameContainer(self)
        privFrameLay = NGridContainer(privFrame)
        privFrameLay.addWidget(self._snmp3Priv,    0,0)
        privFrameLay.addWidget(self._snmp3PrivVal, 0,1)
        self._privShowCheck = QCheckBox('show', self)
        #self._privShowCheck.stateChanged.connect(self._toggleShowPriv)
        privFrameLay.addWidget(self._privShowCheck,  0,2)
        privFrameLay.setColumnStretch(0,0)
        privFrameLay.setColumnStretch(1,1)
        privFrameLay.setHorizontalSpacing(3)

        #self._setSecLevel(AUTH_PRIV)

        self._snmp3Lay.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self._snmp3Lay.addRow(QLabel('Security level:'),   self._snmp3SecLevel)
        self._snmp3Lay.addRow(QLabel('User name:'), self._snmp3User)
        self._snmp3Lay.addRow(self._snmp3AuthLab, authFrame)
        self._snmp3Lay.addRow(self._snmp3PrivLab,         privFrame)


class PermConfigFrame(QGroupBox):
    def __init__(self, parent=None, conf=None):
        super(PermConfigFrame, self).__init__(parent)
        self.setTitle('Permissions')
        grid = NGrid(self)
        grid.addWidget(HelpUtil(self), 0,0)
        grid.addWidget(QListView(self),1,0)


class PropConfigFrame(QGroupBox):
    def __init__(self, parent=None, conf=None):
        super(PropConfigFrame, self).__init__(parent)
        self.setTitle('Properties')
        grid = NGrid(self)
        grid.addWidget(HelpUtil(self), 0,0)
        grid.addWidget(QListView(self),1,0)

class ProbesConfigFrame(QGroupBox):
    def __init__(self, parent=None, conf=None):
        super(ProbesConfigFrame, self).__init__(parent)
        self.setTitle('Probes')
        grid = NGrid(self)
        grid.addWidget(HelpUtil(self), 0,0)
        grid.addWidget(QListView(self),1,0)

class JobsConfigFrame(QGroupBox):
    def __init__(self, parent=None, conf=None):
        super(JobsConfigFrame, self).__init__(parent)
        self.setTitle('Jobs')
        grid = NGrid(self)
        grid.addWidget(HelpUtil(self), 0,0)
        grid.addWidget(QListView(self),1,0)

class HelpUtil(NFrameContainer):
    def __init__(self, parent=None):
        super(HelpUtil, self).__init__(parent)
        grid = NGridContainer(self)
        self._helpButton = QPushButton(self)
        self._helpButton.setFlat(True)
        self._helpButton.setIcon(nocapi.nGetIcon('dialog-information'))
        grid.addWidget(self._helpButton, 0,1)
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,0)
