from PyQt5.QtWidgets   import (
    QAbstractItemView,
    QProgressDialog,
    QSpinBox,
    QDoubleSpinBox,
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
from PyQt5.QtCore import Qt

from sysmo_widgets import NGrid, NFrame, NGridContainer, NFrameContainer
import sysmapi
import monitor.api as monapi
import supercast.main   as supercast


import monitor.commands.net_element_wizard.wizard_pages  as NetElement
import monitor.commands.net_server_wizard.wizard_pages   as SrvElement
import monitor.commands.probe_wizard.wizard_pages        as ProbeElement
import monitor.commands.user_actions_wizard.wizard_pages as UActionPages
import monitor.commands.properties as PropInfo

import monitor.commands.add_element_pages as AddElementPages
from monitor.commands.properties import SnmpConfigFrame

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
TYPE_FIREWALL    = 4
TYPE_PRINTER     = 5
TYPE_OTHER       = 6

class NewTargetDialog(QWizard):
    def __init__(self, parent=None):
        super(NewTargetDialog, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setModal(True)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setPage(1, TargetConfFrame(self))
        self.setStartId(1)
        self.setButtonText(QWizard.FinishButton, 'Validate')
        self.setButtonText(QWizard.CancelButton, 'Close')



class TargetConfFrame(QWizardPage):
    def __init__(self, parent=None):
        super(TargetConfFrame, self).__init__(parent)
        self.setTitle(self.tr('Add new targets'))
        self.setSubTitle('Use this form add new target to the system.')
        grid = NGrid(self)

        formFrame = NFrame(self)
        form = QFormLayout(formFrame)

        otherIcon = sysmapi.nGetIcon('computer')
        srvIcon         = sysmapi.nGetIcon('server')
        routerIcon      = sysmapi.nGetIcon('router')
        switchIcon      = sysmapi.nGetIcon('switch')
        wirelessIcon    = sysmapi.nGetIcon('wireless')
        firewallIcon    = sysmapi.nGetIcon('firewall')
        printerIcon     = sysmapi.nGetIcon('printer')
        self._typeCombo = QComboBox(self)
        self._typeCombo.insertItem(TYPE_SERVER, srvIcon,    'Server')
        self._typeCombo.insertItem(TYPE_ROUTER, routerIcon, 'Router')
        self._typeCombo.insertItem(TYPE_SWITCH, switchIcon, 'Switch')
        self._typeCombo.insertItem(TYPE_WIRELESS, wirelessIcon, 'Wireless router')
        self._typeCombo.insertItem(TYPE_FIREWALL, firewallIcon, 'Firewall')
        self._typeCombo.insertItem(TYPE_PRINTER, printerIcon,  'Printer')
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

        self._latitude = QDoubleSpinBox(self)
        self._latitude.setToolTip('Latitude')
        self._latitude.setDecimals(5)
        self._latitude.setMaximum(90.0)
        self._latitude.setMinimum(-90.0)
        self._longitude = QDoubleSpinBox(self)
        self._longitude.setToolTip('Longitude')
        self._longitude.setDecimals(5)
        self._longitude.setMaximum(180.0)
        self._longitude.setMinimum(-180.0)
        locFrame = NFrameContainer(self)
        locFrameLay = NGridContainer(locFrame)
        locFrameLay.addWidget(self._latitude,  0,0)
        locFrameLay.addWidget(self._longitude, 0,1)
        locFrameLay.setColumnStretch(0,1)
        locFrameLay.setColumnStretch(1,1)
        form.addRow('Location:', locFrame)
        form.addRow(NFrame(self))

        self._snmpEnable    = QCheckBox('SNMP enabled', self)
        self._snmpEnable.stateChanged.connect(self._updateEnable)
        self._snmpEnable.stateChanged.connect(self._formValidate)
        form.addRow(self._snmpEnable)
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
        
        self._versionGroup = QComboBox(self)
        self._versionGroup.insertItem(SNMP_V3, '3')
        self._versionGroup.insertItem(SNMP_V2, '2c')
        self._versionGroup.insertItem(SNMP_V1, '1')
        self._versionGroup.setCurrentIndex(SNMP_V2)
        self._versionGroup.currentIndexChanged.connect(self._updateEnable)
        self._versionGroup.currentIndexChanged.connect(self._formValidate)
        form.addRow('Version:', self._versionGroup)
        self._versionGroupLab  = form.labelForField(self._versionGroup)



        self._community = QLineEdit(self)
        self._community.textChanged.connect(self._formValidate)
        form.addRow('Community:', self._community)
        self._communityLab  = form.labelForField(self._community)

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
        self._authProto.setCurrentIndex(AUTH_MD5)
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
        self._privProto.insertItem(PRIV_AES128, 'AES')
        self._privProto.insertItem(PRIV_DES,    'DES')
        self._privProto.insertSeparator(2)  
        self._privProto.insertItem(PRIV_AES192, 'AES 192')
        self._privProto.insertItem(PRIV_AES256, 'AES 256')
        self._privProto.insertItem(PRIV_3DES,   '3DES')
        self._privProto.setCurrentIndex(PRIV_DES)
        self._privKey   = QLineEdit(self)
        self._privKey.textChanged.connect(self._formValidate)
        self._privKey.setPlaceholderText('Key')
        privFrameLay.addWidget(self._privProto, 0,0)
        privFrameLay.addWidget(self._privKey, 0,1)

        form.addRow('Privacy:', self._privFrame)
        self._privFrameLab = form.labelForField(self._privFrame)

        form.addRow(NFrame(self))
        self._includeICMP    = QCheckBox('Include probe: ICMP Echo presence')
        self._includeIfPerfs = QCheckBox('Include probe: SNMP Interfaces performances')
        self._includeICMP.setChecked(True)
        self._includeIfPerfs.setChecked(True)
        form.addRow(self._includeICMP)
        form.addRow(self._includeIfPerfs)

        grid.addWidget(formFrame, 1,0)

        self._initEnable()
        self._updateEnable()
        self._formValidate()

    def _formValidate(self):
        self.completeChanged.emit()

    def isComplete(self):
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
        print("form snmp valid")
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
            self._privFrameLab,
            self._includeIfPerfs
        ]

        self._stateSnmp2 = [
            self._versionGroup,
            self._versionGroupLab,
            self._port,
            self._portLab,
            self._timeout,
            self._timeoutLab,
            self._community,
            self._communityLab,
            self._includeIfPerfs
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
            self._privFrameLab,
            self._includeIfPerfs
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
            self._authFrameLab,
            self._includeIfPerfs
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
            self._snmp3UserLab,
            self._includeIfPerfs
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

    def validatePage(self):
        props = dict()
        props['host'] = self._hostLine.text()
        props['name'] = self._nameLine.text()
        if self._typeCombo.currentIndex() == TYPE_SERVER:
            props['type'] = 'server'
        elif self._typeCombo.currentIndex() == TYPE_ROUTER:
            props['type'] = 'router'
        elif self._typeCombo.currentIndex() == TYPE_SWITCH:
            props['type'] = 'switch'
        elif self._typeCombo.currentIndex() == TYPE_WIRELESS:
            props['type'] = 'wireless'
        elif self._typeCombo.currentIndex() == TYPE_FIREWALL:
            props['type'] = 'firewall'
        elif self._typeCombo.currentIndex() == TYPE_PRINTER:
            props['type'] = 'printer'
        else:
            props['type'] = 'other'

        props['latitude'] = str(self._latitude.value())
        props['longitude'] = str(self._longitude.value())

        sprops = dict()
        if self._snmpEnable.isChecked() == True:
            sprops['snmp_port']     = str(self._port.value())
            sprops['snmp_timeout']  = str(self._timeout.value())
            if self._versionGroup.currentIndex() == SNMP_V3:
                sprops['snmp_version'] = '3'
                sprops['snmp_usm_user'] = self._snmp3User.text()
                if self._secLevel.currentIndex() == NO_AUTH_NO_PRIV:
                    sprops['snmp_seclevel'] = 'noAuthNoPriv'
                else:
                    sprops['snmp_seclevel'] = 'authNoPriv'
                    sprops['snmp_authkey'] = self._authKey.text()
                    if self._authProto.currentIndex() == AUTH_SHA:
                        sprops['snmp_authproto'] = 'SHA'
                    elif self._authProto.currentIndex() == AUTH_MD5:
                        sprops['snmp_authproto'] = 'MD5'

                    if self._secLevel.currentIndex() == AUTH_PRIV:
                        sprops['snmp_seclevel'] = 'authPriv'
                        sprops['snmp_privkey']  = self._privKey.text()
                        if self._privProto.currentIndex() == PRIV_AES128:
                            sprops['snmp_privproto'] = 'AES'
                        elif self._privProto.currentIndex() == PRIV_DES:
                            sprops['snmp_privproto'] = 'DES'
                        elif self._privProto.currentIndex() == PRIV_AES192:
                            sprops['snmp_privproto'] = 'AES192'
                        elif self._privProto.currentIndex() == PRIV_AES256:
                            sprops['snmp_privproto'] = 'AES256'
                        elif self._privProto.currentIndex() == PRIV_3DES:
                            sprops['snmp_privproto'] = '3DES'
            else:
                if self._versionGroup.currentIndex() == SNMP_V2:
                    sprops['snmp_version'] = '2c'
                else:
                    sprops['snmp_version'] = '1'

                sprops['snmp_community'] = self._community.text()

        sprops
        props
        withsnmp = self._snmpEnable.isChecked()
        picmp = self._includeICMP.isChecked()
        psnmp = self._includeIfPerfs.isChecked()

        win = CreateTargetDialog(withsnmp, picmp, psnmp, props, sprops, self)
        return False


    def mousePressEvent(self, event):   pass
    def mouseReleaseEvent(self, event): pass


class CreateTargetDialog(QProgressDialog):
    def __init__(self, withsnmp, probeicmp, probeifperf, props, sprops, parent=None):
        super(CreateTargetDialog, self).__init__(parent)
        self.setMinimum(0)
        self.setMaximum(0)
        self.setModal(True)
        self._props = props
        self._sprops = sprops
        self._picmp = probeicmp
        self._psnmp = probeifperf
        self._ifSelection = None

        if withsnmp == False:
            self._createTargetQuery()
        else:
           self._elementInterfaceQuery()
        self.show()

    def _elementInterfaceQuery(self):
        self.setLabel(QLabel('Getting SNMP interfaces informations...',self))
        supercast.send(
            'monitorElementInterfaceQuery',
            (
                self._sprops,
                self._props
            ),
            self._elementInterfaceReply
        )

    def _elementInterfaceReply(self, reply):
        if reply['value']['status'] == False:
            err = QMessageBox(self)
            err.setModal(True)
            err.setIconPixmap(sysmapi.nGetPixmap('dialog-information'))
            err.setText("Snmp manager failed to get information for element:")
            err.setInformativeText("ERROR: " + reply['value']['reply'])
            err.finished[int].connect(self._closeMe)
            err.open()
            return

        SelectInterfaceDialog(reply['value']['reply'], self)

    def _closeMe(self):
        self.deleteLater()

    def _createTargetQuery(self):
        self.setLabel(QLabel('Create target...',self))
        supercast.send(
            'monitorCreateTargetQuery',
            (
                self._sprops,
                self._props
            ),
            self._createTargetReply
        )

    def _createTargetReply(self, reply):
        if reply['value']['status'] == True:
            self._targetName = reply['value']['reply']
        else:
            err = QMessageBox(self)
            err.setModal(True)
            err.setIconPixmap(sysmapi.nGetPixmap('dialog-information'))
            err.setText("Monitor failed to create target:")
            err.setInformativeText("ERROR: " + reply['value']['reply'])
            err.finished[int].connect(self._closeMe)
            err.open()
            return

        if self._picmp == True:
            self._createIcmpQuery()
        elif self._ifSelection != None:
            self._createIfPerfQuery()
        else:
            self.deleteLater()

    def _createIcmpQuery(self):
        supercast.send(
            'monitorCreateNchecksQuery',
            (
                self._targetName,
                'icmp',
                dict()
            ),
            self._createIcmpReply
        )

    def _createIcmpReply(self, msg):
        print(("reply icmp: ", msg))
        if self._ifSelection != None:
            self._createIfPerfQuery()
        else:
            self.deleteLater()

    def _createIfPerfQuery(self):
        supercast.send(
            'monitorCreateIfPerfQuery',
            (
                self._targetName,
                self._ifSelection
            ),
            self._createIfPerfReply
        )

    def _createIfPerfReply(self, msg):
        self.deleteLater()


    def setIfSelection(self, selection):
        self._ifSelection = selection
        self._createTargetQuery()

class SelectInterfaceDialog(QDialog):
    def __init__(self, ifInfos, parent):
        super(SelectInterfaceDialog, self).__init__(parent)
        self._ifInfos = ifInfos
        self.setModal(True)
        self.show()
        self._grid = NGrid(self)
        self.setLayout(self._grid)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        okbutton = buttonBox.button(QDialogButtonBox.Ok)
        okbutton.clicked.connect(self._validate)
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
        ifLayout.addWidget(buttonBox)

        self._grid.addWidget(infoFrame,  0,0)
        self._grid.addWidget(ifFrame,    1,0)

        self._initializePage()

    def _validate(self):
        count = self._treeWidget.topLevelItemCount()
        selectedIfs = list()
        for index in range(count):
            item = self._treeWidget.topLevelItem(index)
            if (item.checkState(0) == Qt.Checked):
                selectedIfs.append(int(item.text(5)))

        self.parent().setIfSelection(selectedIfs)
        self.deleteLater()

    def _initializePage(self):
        self._treeWidget.clear()
        ifInfos = self._ifInfos
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




