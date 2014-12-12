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

class NewTargetDialog(QMenu):
    def __init__(self, parent=None):
        super(NewTargetDialog, self).__init__(parent)
        action = QWidgetAction(self)
        action.setDefaultWidget(NewTargetFrame(self))
        self.addAction(action)

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

class NewTargetFrame(NFrame):
    def __init__(self, parent=None):
        super(NewTargetFrame, self).__init__(parent)
        grid = NGrid(self)

        lab = QLabel('<h2>%s</h2>' % 'Add a new target', self)
        grid.addWidget(lab, 0,0)



        formFrame = NFrame(self)
        form = QFormLayout(formFrame)
        self._hostLine = QLineEdit(self)
        self._hostLine.setPlaceholderText('ipv4, ipv6 or hostname')
        self._hostLine.setToolTip('ipv4, ipv6 or hostname')
        form.addRow('Host:', self._hostLine)
        self._typeCombo = QComboBox(self)
        form.addRow('Type:', self._typeCombo)
        self._nameLine = QLineEdit(self)
        form.addRow('Name:', self._nameLine)

        form.addRow(NFrame(self))

        snmpEnable    = QCheckBox('SNMP enabled', self)
        snmpEnable.stateChanged[int].connect(self._updateEnable)
        form.addRow(snmpEnable)

        self._versionGroup = QComboBox(self)
        self._versionGroup.insertItem(SNMP_V3, '3')
        self._versionGroup.insertItem(SNMP_V2, '2c')
        self._versionGroup.insertItem(SNMP_V1, '1')
        self._versionGroup.setCurrentIndex(SNMP_V2)
        self._versionGroup.currentIndexChanged[int].connect(self._updateEnable)
        form.addRow('Version:', self._versionGroup)

        self._port = QSpinBox(self)
        self._port.setMinimum(1)
        self._port.setMaximum(65535)
        self._port.setValue(161)
        form.addRow('Port:', self._port)

        self._timeout = QSpinBox(self)
        self._timeout.setToolTip('Snmp timeout in milliseconds')
        self._timeout.setMinimum(100)
        self._timeout.setMaximum(20000)
        self._timeout.setValue(2500)
        form.addRow('Timeout:', self._timeout)
        
        form.addRow(NFrame(self))

        self._community = QLineEdit(self)
        form.addRow('Community:', self._community)

        form.addRow(NFrame(self))

        self._secLevel = QComboBox(self)
        self._secLevel.insertItem(AUTH_PRIV, 'authPriv')
        self._secLevel.insertItem(AUTH_NO_PRIV, 'authNoPriv')
        self._secLevel.insertItem(NO_AUTH_NO_PRIV, 'noAuthNoPriv')
        self._secLevel.setCurrentIndex(NO_AUTH_NO_PRIV)
        self._secLevel.currentIndexChanged[int].connect(self._updateEnable)


        form.addRow('Sec level:', self._secLevel)

        self._snmp3User = QLineEdit(self)
        form.addRow('User:', self._snmp3User)

        authFrame = NFrameContainer(self)
        authFrameLay = NGridContainer(authFrame)
        self._authProto = QComboBox(self)
        self._authProto.setFixedWidth(100)
        self._authProto.insertItem(AUTH_SHA, 'SHA')
        self._authProto.insertItem(AUTH_MD5, 'MD5')
        self._authKey   = QLineEdit(self)
        self._authKey.setPlaceholderText('Key')
        authFrameLay.addWidget(self._authProto, 0,0)
        authFrameLay.addWidget(self._authKey, 0,1)

        form.addRow('Authentication:', authFrame)

        privFrame = NFrameContainer(self)
        privFrameLay = NGridContainer(privFrame)
        self._privProto = QComboBox(self)
        self._privProto.setFixedWidth(100)
        self._privProto.insertItem(PRIV_AES128, 'AES (128)')
        self._privProto.insertItem(PRIV_DES,    'DES')
        self._privProto.insertSeparator(2)  
        self._privProto.insertItem(PRIV_AES192, 'AES 192')
        self._privProto.insertItem(PRIV_AES256, 'AES 256')
        self._privProto.insertItem(PRIV_3DES,   '3DES')
        self._privKey   = QLineEdit(self)
        self._privKey.setPlaceholderText('Key')
        privFrameLay.addWidget(self._privProto, 0,0)
        privFrameLay.addWidget(self._privKey, 0,1)

        form.addRow('Privacy:', privFrame)

        grid.addWidget(formFrame, 1,0)




        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton('Cancel', QDialogButtonBox.RejectRole)
        buttonBox.addButton('Apply', QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self._accepted)
        buttonBox.rejected.connect(self._rejected)
        grid.addWidget(buttonBox, 2,0)


    def _updateEnable(self, val):
        print "hello enable"

    def mousePressEvent(self, event):   pass
    def mouseReleaseEvent(self, event): pass

    def _snmpCheck(self, event):
        print "check"

    def _accepted(self):
        self.parent().hide()

    def _rejected(self):
        print "rejected"
        self.parent().hide()



class AddElementWizard(QDialog):
    def __init__(self, parent=None):
        super(AddElementWizard, self).__init__(parent)
        grid = NGridContainer(self)
        grid.addWidget(PropInfo.PropertiesAll(self))


# NEW WIZARD
class AddElementWizard2(QWizard):
    def __init__(self, parent=None):
        super(AddElementWizard2, self).__init__(parent)
        self._sysInfo   = None
        self._ifInfo    = None
        self._engineId  = None

        #self.setWizardStyle(QWizard.ModernStyle)
        #self.setPixmap(QWizard.WatermarkPixmap, nocapi.nGetPixmap('network-bay'))

        self.setModal(True)
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        npage1  = AddElementPages.Page10(self)
        npage2  = AddElementPages.Page20(self)
        npage3  = AddElementPages.Page30(self)
        self.setPage(10, npage1)
        self.setPage(20, npage2)
        self.setPage(30, npage3)
        self.setStartId(10)

    def setSysInfo(self, info):
        self._sysInfo = info

    def setIfInfo(self, info):
        self._ifInfo = info

    def setEngineId(self, info):
        self._engineId = info

    def setIfSelection(self, selection):
        self._ifSelection = selection





# OLD WIZARDS
class UserActionsWizard(QWizard):
    def __init__(self, parent=None, element=None):
        super(UserActionsWizard, self).__init__(parent)

        self.setModal(True)
        page1 = UActionPages.Page1(self, element)
        self.setPage(1, page1)
        self.setStartId(1)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.WatermarkPixmap, nocapi.nGetPixmap('console'))
        self.setPixmap(QWizard.LogoPixmap,nocapi.nGetPixmap('applications-system'))
        self.show()

class ProbeWizard(QWizard):
    def __init__(self, defs, key, parent, pyCall, defaultIp=None):
        super(ProbeWizard, self).__init__(parent)
        self._callback = pyCall
        #self.setFixedWidth(800)
        self.setModal(True)
        self.probeKey   = key
        self.defaultIp  = defaultIp
        self.defs       = defs
        ppage1 = ProbeElement.Page1(self)
        ppage2 = ProbeElement.Page2(self)
        ppage3 = ProbeElement.Page3(self)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setPage(1, ppage1)
        self.setPage(2, ppage2)
        self.setPage(3, ppage3)
        self.setStartId(1)
        self.page1_config = None
        self.page3_config = None
        self.setPixmap(QWizard.WatermarkPixmap, nocapi.nGetPixmap('radar'))
        self.setPixmap(QWizard.LogoPixmap,nocapi.nGetPixmap('applications-system'))
        # page2 use QWizard.registerField
        # self.page2_config = None 
        self.show()

    def validateConfig(self):
        checkDef = dict()
        checkDef['def']     = self.page1_config
        checkDef['display_name'] = self.field('p2_display_name')
        checkDef['step']    = self.field('p2_check_step')
        checkDef['alert']   = self.page3_config
        checkDef['exe']     = self.probeKey

        descr   = self.field('p2_description')
        if descr == None:
            checkDef['descr'] = ""
        else:
            checkDef['descr'] = descr

        self._callback(checkDef)

class NetworkElementWizard(QWizard):
    def __init__(self, parent=None):
        super(NetworkElementWizard, self).__init__(parent)

        self._sysInfo   = None
        self._ifInfo    = None
        self._engineId  = None

        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.WatermarkPixmap, nocapi.nGetPixmap('network-bay'))

        self.setModal(True)
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        npage1  = NetElement.Page1(self)
        npage2  = NetElement.Page2(self)
        npage3  = NetElement.Page3(self)
        self.setPage(1, npage1)
        self.setPage(2, npage2)
        self.setPage(3, npage3)
        self.setStartId(1)

    def setSysInfo(self, info):
        self._sysInfo = info

    def setIfInfo(self, info):
        self._ifInfo = info

    def setEngineId(self, info):
        self._engineId = info

    def setIfSelection(self, selection):
        self._ifSelection = selection

        
class NetworkServerWizard(QWizard):
    def __init__(self, parent=None):
        super(NetworkServerWizard, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.WatermarkPixmap, nocapi.nGetPixmap('server-bay'))

        self.setModal(True)
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        npage1   = SrvElement.Page1(self)
        self.setPage(1, npage1)
        self.setStartId(1)
