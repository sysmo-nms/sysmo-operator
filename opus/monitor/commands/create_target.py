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
import supercast.main   as supercast


class Wizard(QWizard):
    NetElement  = 11
    NetService  = 21
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        self._configType = None
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.HaveHelpButton,          True)
        self.setOption(QWizard.HelpButtonOnRight,       False)

        self.setButtonText(QWizard.CancelButton, self.tr("&Close"))
        self.setButtonText(QWizard.FinishButton, self.tr("&Apply"))

        page1   = ChooseType(self)
        page2   = CreateNetworkElement(self)
        page3   = CreateNetworkServer(self)

        self.setPage(1,  page1)
        self.setPage(11, page2)
        self.setPage(21, page3)
        self.setStartId(1)

        self.show()


class ChooseType(QWizardPage):
    def __init__(self, parent=None):
        super(ChooseType, self).__init__(parent)
        self._configType = Wizard.NetElement
        chooseTypeLayout    = NGrid(self)
        self._parent = parent
        self.setTitle(self.tr('Create target wizard'))
        self.setSubTitle(self.tr('Choose the type of target you want to create'))

        typeNetElement      = QCommandLinkButton(self)
        typeNetElement.setMaximumHeight(200)
        typeNetElement.setText('Network element')
        typeNetElement.setDescription(self.tr('''
            Using this wizard will help you to create a network element target.
            Network elements have the common particularity to support SNMP
            protocol and the MIB-2 management information base. This allow
            to fetch interfaces performance informations for example, and then
            generate nice graphs.
        '''))
        typeNetElement.clicked.connect(self._startNetElement)

        typeNetService      = QCommandLinkButton(self)
        typeNetService.setMaximumHeight(200)
        typeNetService.setText('Network server')
        typeNetService.setDescription(self.tr('''
            Create a network server target, and get live status of services.
            This wizard will help you to create a network server target.
            The common particularity of a server is that it fullfil one or
            more services like HTTP, SMTP or others. A network server may
            have SNMP support for one of his services, but the SNMP query
            must be configured manualy. If you know that your server support
            the MIB-2 management information base, you can apply a template
            configuration common to the network elements.
        '''))
        typeNetService.clicked.connect(self._startNetService)

        chooseTypeLayout.addWidget(typeNetElement, 0,0)
        chooseTypeLayout.addWidget(typeNetService, 1,0)
        chooseTypeLayout.setRowStretch(0,1)
        chooseTypeLayout.setRowStretch(1,1)

        self.setLayout(chooseTypeLayout)

    def _startNetElement(self):
        self._configType = Wizard.NetElement
        self._parent.next()

    def _startNetService(self):
        self._configType = Wizard.NetService
        self._parent.next()

    def nextId(self):
        return self._configType


class CreateNetworkElement(QWizardPage):
    SNMP_V2  = 0
    SNMP_V3  = 1
    IP_V4    = 0
    IP_V6    = 1
    def __init__(self, parent=None):
        super(CreateNetworkElement, self).__init__(parent)
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

        self._snmpButton = QComboBox(self)
        self._snmpButton.insertItem(self.SNMP_V2, 'SNMP version 2b')
        self._snmpButton.insertItem(self.SNMP_V3, 'SNMP version 3')

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
        


class CreateNetworkServer(QWizardPage):
    IP_V4    = 0
    IP_V6    = 1
    NAME_MANUAL  = 0
    NAME_DYNAMIC = 1
    def __init__(self, parent=None):
        super(CreateNetworkServer, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network server to the main configuration
        '''))
        self.setFinalPage(True)

        layout = NGrid(self)
        layout.setContentsMargins(0,15,0,0)
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
        self._ipButton.insertItem(self.IP_V4, 'IP version 4')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6')

        self._nameButton = QComboBox(self)
        self._nameButton.insertItem(self.NAME_MANUAL,  'Manual name')
        self._nameButton.insertItem(self.NAME_DYNAMIC, 'Dynamic DNS name')
        self._nameLine  = QLineEdit(self)


        probeFrame  = NFrameContainer(self)
        probeGrid   = NGridContainer(probeFrame)

        probeCommFrame  = NFrameContainer(self)
        probeCommGrid   = NGridContainer(probeCommFrame)
        probeCommGrid.setColumnStretch(0, 0)
        probeCommGrid.setColumnStretch(1, 1)
        probeAdd        = QPushButton(self)
        probeAdd.setIcon(nocapi.nGetIcon('list-add'))
        probeCommGrid.addWidget(probeAdd, 0,0)
        probeCommFrame.setLayout(probeCommGrid)

        probeTable = QTreeWidget(self)
        probeTable.setColumnCount(4)
        probeTable.setHeaderLabels(['Active probes', 'Module', 'Raise alerts', 'Set property'])
        go_icmp = QTreeWidgetItem(probeTable)
        go_icmp.setText(0, 'Generic ICMP check')
        go_icmp.setText(1, 'go_check_icmp')
        go_icmp.setText(2, 'Yes')
        go_icmp.setText(3, 'No')
        icmp_desc = 'Check icmp reply every 30 seconds and alert on failure'
        go_icmp.setToolTip(0, icmp_desc)
        go_icmp.setToolTip(1, icmp_desc)
        go_icmp.setToolTip(2, icmp_desc)
        go_icmp.setToolTip(3, icmp_desc)

        go_dns = QTreeWidgetItem(probeTable)
        go_dns.setText(0, 'Reverse DNS lookup')
        go_dns.setText(1, 'go_check_dns')
        go_dns.setText(2, 'Yes')
        go_dns.setText(3, 'Yes: hostname')
        dns_desc = '''
- Set the hostname property of the host accordingly to the
reverse dns lookup.
- Alert every time the value returned by the DNS does not
match the preceding value. 
- DOES NOT raise an alert on DNS query error or timeout.
'''
        go_dns.setToolTip(0, dns_desc)
        go_dns.setToolTip(1, dns_desc)
        go_dns.setToolTip(2, dns_desc)
        go_dns.setToolTip(3, dns_desc)
        #probeList.addItem(QListWidgetItem('go_check_icmp'))
        #probeList.addItem(QListWidgetItem('go_check_dns'))
        #probeList.addItem(QListWidgetItem('go_check_tcp'))

        probeGrid.addWidget(probeCommFrame, 0,0)
        probeGrid.addWidget(probeTable,     1,0)





        tempLayout.addWidget(self._ipButton,    0,0)
        tempLayout.addWidget(self._ipLine,      0,1)
        tempLayout.addWidget(self._nameButton,  1,0)
        tempLayout.addWidget(self._nameLine,    1,1)
        tempLayout.addWidget(probeFrame,        2,0,1,2)


        #tempLayout.setAlignment(self._nameButton, Qt.AlignVCenter)
        tempLayout.setColumnStretch(0,0)
        tempLayout.setColumnStretch(1,1)
        return tempFrame

    def nextId(self):
        return -1

    def validatePage(self):
        print "send"
        ret = supercast.send(
            'query',
            'getChecksInfo',
            self.monitorReply
        )
        return False

    def _assertCmd(self, a,b,c,d,e): return True

    def monitorReply(self, msg):
        print "get reply!!!!!!", msg
