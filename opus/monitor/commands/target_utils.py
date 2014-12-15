from PySide.QtGui   import (
    QSpinBox,
    QDialog,
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
    QMessageBox,
    QMenu,
    QWidgetAction,
    QDialogButtonBox
)
from PySide.QtCore import Qt

from noctopus_widgets import NGrid, NFrame, NGridContainer, NFrameContainer
import nocapi
import opus.monitor.api as monapi
import supercast.main   as supercast


import opus.monitor.commands.net_element_wizard.wizard_pages  as NetElement
import opus.monitor.commands.net_server_wizard.wizard_pages   as SrvElement
import opus.monitor.commands.probe_wizard.wizard_pages        as ProbeElement
import opus.monitor.commands.user_actions_wizard.wizard_pages as UActionPages
import opus.monitor.commands.properties as PropInfo

import opus.monitor.commands.add_element_pages as AddElementPages
from opus.monitor.commands.properties import SnmpConfigFrame

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

AUTH_PRIV       = 2
AUTH_NO_PRIV    = 1
NO_AUTH_NO_PRIV = 0

TYPE_SERVER      = 0
TYPE_ROUTER      = 1
TYPE_SWITCH      = 2
TYPE_WIRELESS    = 3
TYPE_OTHER       = 4

class NewTargetDialog(QMenu):
    def __init__(self, parent=None):
        super(NewTargetDialog, self).__init__(parent)
        action = QWidgetAction(self)
        action.setDefaultWidget(TargetConfFrame(self))
        self.addAction(action)

class TargetConfFrame(NFrame):
    def __init__(self, parent=None):
        super(TargetConfFrame, self).__init__(parent)
        grid = NGrid(self)

        lab = QLabel('<h2>%s</h2>' % 'Add a new target', self)
        grid.addWidget(lab, 0,0)

        formFrame = NFrame(self)
        form = QFormLayout(formFrame)

        otherIcon = nocapi.nGetIcon('computer')
        srvIcon = nocapi.nGetIcon('network-server')
        routerIcon = nocapi.nGetPixmap('router')
        switchIcon = nocapi.nGetPixmap('switch')
        wirelessIcon = nocapi.nGetPixmap('wireless')
        self._typeCombo = QComboBox(self)
        self._typeCombo.insertItem(TYPE_SERVER, srvIcon,    'Server')
        self._typeCombo.insertItem(TYPE_ROUTER, routerIcon, 'Router')
        self._typeCombo.insertItem(TYPE_SWITCH, switchIcon, 'Switch')
        self._typeCombo.insertItem(TYPE_WIRELESS, wirelessIcon, 'Wireless router')
        self._typeCombo.insertItem(TYPE_OTHER, otherIcon,   'Other')
        form.addRow('Type:', self._typeCombo)

        self._hostLine = QLineEdit(self)
        self._hostLine.textChanged.connect(self._formValidate)
        self._hostLine.setPlaceholderText('ipv4, ipv6 or hostname')
        self._hostLine.setToolTip('ipv4, ipv6 or hostname')
        form.addRow('Host:', self._hostLine)

        self._nameLine = QLineEdit(self)
        self._nameLine.textChanged.connect(self._formValidate)
        form.addRow('Name:', self._nameLine)

        form.addRow(NFrame(self))

        self._snmpEnable    = QCheckBox('SNMP enabled', self)
        self._snmpEnable.stateChanged.connect(self._updateEnable)
        self._snmpEnable.stateChanged.connect(self._formValidate)
        form.addRow(self._snmpEnable)

        self._versionGroup = QComboBox(self)
        self._versionGroup.insertItem(SNMP_V3, '3')
        self._versionGroup.insertItem(SNMP_V2, '2c')
        self._versionGroup.insertItem(SNMP_V1, '1')
        self._versionGroup.setCurrentIndex(SNMP_V2)
        self._versionGroup.currentIndexChanged.connect(self._updateEnable)
        self._versionGroup.currentIndexChanged.connect(self._formValidate)
        form.addRow('Version:', self._versionGroup)
        self._versionGroupLab  = form.labelForField(self._versionGroup)

        self._port = QSpinBox(self)
        self._port.setMinimum(1)
        self._port.setMaximum(65535)
        self._port.setValue(161)
        form.addRow('Port:', self._port)
        self._portLab  = form.labelForField(self._port)

        self._timeout = QSpinBox(self)
        self._timeout.setToolTip('Snmp timeout in milliseconds')
        self._timeout.setMinimum(100)
        self._timeout.setMaximum(20000)
        self._timeout.setValue(2500)
        form.addRow('Timeout:', self._timeout)
        self._timeoutLab  = form.labelForField(self._timeout)
        
        form.addRow(NFrame(self))

        self._community = QLineEdit(self)
        self._community.textChanged.connect(self._formValidate)
        form.addRow('Community:', self._community)
        self._communityLab  = form.labelForField(self._community)

        form.addRow(NFrame(self))

        self._secLevel = QComboBox(self)
        self._secLevel.insertItem(NO_AUTH_NO_PRIV, 'noAuthNoPriv')
        self._secLevel.insertItem(AUTH_NO_PRIV, 'authNoPriv')
        self._secLevel.insertItem(AUTH_PRIV, 'authPriv')
        self._secLevel.setCurrentIndex(NO_AUTH_NO_PRIV)
        self._secLevel.currentIndexChanged.connect(self._updateEnable)
        self._secLevel.currentIndexChanged.connect(self._formValidate)
        form.addRow('Sec level:', self._secLevel)
        self._secLevelLab = form.labelForField(self._secLevel)

        self._snmp3User = QLineEdit(self)
        self._snmp3User.textChanged.connect(self._formValidate)
        form.addRow('User:', self._snmp3User)
        self._snmp3UserLab = form.labelForField(self._snmp3User)

        self._authFrame = NFrameContainer(self)
        authFrameLay = NGridContainer(self._authFrame)
        self._authProto = QComboBox(self)
        self._authProto.setFixedWidth(100)
        self._authProto.insertItem(AUTH_SHA, 'SHA')
        self._authProto.insertItem(AUTH_MD5, 'MD5')
        self._authKey   = QLineEdit(self)
        self._authKey.textChanged.connect(self._formValidate)
        self._authKey.setPlaceholderText('Key')
        authFrameLay.addWidget(self._authProto, 0,0)
        authFrameLay.addWidget(self._authKey, 0,1)
        form.addRow('Authentication:', self._authFrame)
        self._authFrameLab = form.labelForField(self._authFrame)

        self._privFrame = NFrameContainer(self)
        privFrameLay = NGridContainer(self._privFrame)
        self._privProto = QComboBox(self)
        self._privProto.setFixedWidth(100)
        self._privProto.insertItem(PRIV_AES128, 'AES (128)')
        self._privProto.insertItem(PRIV_DES,    'DES')
        self._privProto.insertSeparator(2)  
        self._privProto.insertItem(PRIV_AES192, 'AES 192')
        self._privProto.insertItem(PRIV_AES256, 'AES 256')
        self._privProto.insertItem(PRIV_3DES,   '3DES')
        self._privKey   = QLineEdit(self)
        self._privKey.textChanged.connect(self._formValidate)
        self._privKey.setPlaceholderText('Key')
        privFrameLay.addWidget(self._privProto, 0,0)
        privFrameLay.addWidget(self._privKey, 0,1)

        form.addRow('Privacy:', self._privFrame)
        self._privFrameLab = form.labelForField(self._privFrame)

        grid.addWidget(formFrame, 1,0)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal)
        buttonBox.accepted.connect(self._accepted)
        buttonBox.rejected.connect(self._rejected)
        grid.addWidget(buttonBox, 2,0)
        self._validate = buttonBox.button(QDialogButtonBox.Ok)

        self._initEnable()
        self._updateEnable()
        self._formValidate()

    def _formValidate(self):
        if self._formIsValid() == True:
            self._validate.setEnabled(True)
        else:
            self._validate.setEnabled(False)
        
    def _formIsValid(self):
        if self._snmpEnable.isChecked() == False:
            return self._formGeneralValid()

        if self._formGeneralValid() == True:
            return self._formSnmpValid()

        return False

    def _formGeneralValid(self):
        if self._hostLine.text() == "": return False
        if self._nameLine.text() == "": return False
        return True

    def _formSnmpValid(self):
        print "form snmp valid"
        if self._versionGroup.currentIndex() == SNMP_V3:
            if self._snmp3User.text() == "": return False
            if self._secLevel.currentIndex() == AUTH_NO_PRIV:
                if self._authKey.text() == "" or len(self._authKey.text()) < 8: return False
            elif self._secLevel.currentIndex() == AUTH_PRIV:
                if self._authKey.text() == "" or (len(self._authKey.text()) < 8): return False
                if self._privKey.text() == "" or (len(self._privKey.text()) < 8): return False
        else:
            if self._community.text() == "": return False
        return True

    def _initEnable(self):
        self._stateSnmp = [
            self._versionGroup,
            self._versionGroupLab,
            self._port,
            self._portLab,
            self._timeout,
            self._timeoutLab,
            self._community,
            self._communityLab,
            self._secLevel,
            self._secLevelLab,
            self._snmp3User,
            self._snmp3UserLab,
            self._authFrame,
            self._authFrameLab,
            self._privFrame,
            self._privFrameLab
        ]

        self._stateSnmp2 = [
            self._versionGroup,
            self._versionGroupLab,
            self._port,
            self._portLab,
            self._timeout,
            self._timeoutLab,
            self._community,
            self._communityLab
        ]

        self._stateSnmp3AuthPriv = [
            self._versionGroup,
            self._versionGroupLab,
            self._port,
            self._portLab,
            self._timeout,
            self._timeoutLab,
            self._secLevel,
            self._secLevelLab,
            self._snmp3User,
            self._snmp3UserLab,
            self._authFrame,
            self._authFrameLab,
            self._privFrame,
            self._privFrameLab
        ]

        self._stateSnmp3AuthNoPriv = [
            self._versionGroup,
            self._versionGroupLab,
            self._port,
            self._portLab,
            self._timeout,
            self._timeoutLab,
            self._secLevel,
            self._secLevelLab,
            self._snmp3User,
            self._snmp3UserLab,
            self._authFrame,
            self._authFrameLab
        ]

        self._stateSnmp3NoAuthNoPriv = [
            self._versionGroup,
            self._versionGroupLab,
            self._port,
            self._portLab,
            self._timeout,
            self._timeoutLab,
            self._secLevel,
            self._secLevelLab,
            self._snmp3User,
            self._snmp3UserLab
        ]

    def _updateEnable(self):
        if self._snmpEnable.isChecked() == False:
            for element in self._stateSnmp:
                element.setEnabled(False)
            return

        if self._versionGroup.currentIndex() == SNMP_V1:
            for element in self._stateSnmp:
                element.setEnabled(False)
            for element in self._stateSnmp2:
                element.setEnabled(True)
            return
        elif self._versionGroup.currentIndex() == SNMP_V2:
            for element in self._stateSnmp:
                element.setEnabled(False)
            for element in self._stateSnmp2:
                element.setEnabled(True)
            return
        else:
            if self._secLevel.currentIndex() == AUTH_PRIV:
                for element in self._stateSnmp:
                    element.setEnabled(False)
                for element in self._stateSnmp3AuthPriv:
                    element.setEnabled(True)
                return
            elif self._secLevel.currentIndex() == AUTH_NO_PRIV:
                for element in self._stateSnmp:
                    element.setEnabled(False)
                for element in self._stateSnmp3AuthNoPriv:
                    element.setEnabled(True)
                return
            else:
                for element in self._stateSnmp:
                    element.setEnabled(False)
                for element in self._stateSnmp3NoAuthNoPriv:
                    element.setEnabled(True)
                return

    def _accepted(self):
        print "accept..."

    def _rejected(self):
        self.parent().hide()

    def mousePressEvent(self, event):   pass
    def mouseReleaseEvent(self, event): pass
