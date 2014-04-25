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
    QListWidget,
    QListWidgetItem,
    QMessageBox
)
from PySide.QtCore import Qt

from noctopus_widgets import NGrid, NFrame
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
    V2  = 2
    V3  = 3
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
        self._ipButton.addItem('IP version 4:')
        self._ipButton.addItem('IP version 6:')

        self._snmpButton = QComboBox(self)
        self._snmpButton.addItem('SNMP version 2b')
        self._snmpButton.addItem('SNMP version 3')
        self._snmpButton.addItem('Do not use SNMP')
        self._tpButton  = QComboBox(self)
        self._tpButton.addItem('Add a template')
        self._templateList = self._initTempList()

        tempLayout.addWidget(self._ipButton,                            0,0)
        tempLayout.addWidget(self._ipLine,                              0,1)
        tempLayout.addWidget(self._snmpButton,                          1,0)
        tempLayout.addWidget(self._initSnmpFrame(),                     1,1,2,1)
        tempLayout.addWidget(self._tpButton,                            3,0)
        tempLayout.addWidget(self._templateList,                        3,1,2,1)

        tempLayout.addWidget(QPushButton('Show details', self),         5,0)

        tempLayout.setAlignment(self._snmpButton, Qt.AlignVCenter)
        tempLayout.setColumnStretch(0,0)
        tempLayout.setColumnStretch(1,1)
        return tempFrame

    def _initTempList(self):
        listW = QListWidget(self)
        testItem = QListWidgetItem()
        testItem.setText('Standard ICMP element')
        testItem.setIcon(nocapi.nGetIcon('text-x-generic-template'))
        testItem2 = QListWidgetItem()
        testItem2.setIcon(nocapi.nGetIcon('text-x-generic-template'))
        testItem2.setText('Standard SNMP element')
        listW.insertItem(0,testItem)
        listW.insertItem(1,testItem2)
        listW.setAlternatingRowColors(True)
        return listW


    def _initPropertiesFrame(self):
        propFrame = QGroupBox(self)
        propFrame.setTitle(self.tr("&Properties"))
        propLayout = QGridLayout(propFrame)
        propLayout.setColumnStretch(0,0)
        propLayout.setColumnStretch(1,1)
        propFrame.setLayout(propLayout)

        addButton = QPushButton(self)
        addButton.setIcon(nocapi.nGetIcon('list-add'))
        propLayout.addWidget(addButton,             0,0)
        propLayout.addWidget(QListWidget(self),   1,0,1,2)

        return propFrame

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

    def _initProbesFrame(self):
        probesFrame = QGroupBox(self)
        probesFrame.setTitle(self.tr("P&robes"))
        probesGrid = NGrid(probesFrame)
        probesGrid.addWidget(QListWidget(probesFrame))
        probesFrame.setLayout(probesGrid)
        return probesFrame

    def nextId(self):
        return -1

    def validatePage(self):
        #snmpV2Read  = self._snmpV2Read.text()
        #snmpV2Write = self._snmpV2Write.text()
        #ip          = self._ipLine.text()
        #snmpV2Read  = self._snmpV2Read.text()
        #snmpV2Write = self._snmpV2Write.text()
        ip          = "192.168.0.5"
        perms       = (["admin"], ["admin"])
        tpl         = "Generic SNMP element"
        ro          = "public"
        rw          = "public"

        ret = supercast.send(
            'monitorCreateTarget', 
            (ip, perms, ro, rw, tpl),
            self.monitorReply
        )

        #self.dial = QMessageBox(self)
        #self.dial.setModal(True)
        #self.dial.setText(self.tr('Waiting for server response'))
        #button = self.dial.buttons()
        #button.setDisabled(True)
        #self.dial.exec_()

        return False

    def monitorReply(self, msg):
        print "get reply!!!!!!", msg
        


class CreateNetworkServer(QWizardPage):
    def __init__(self, parent=None):
        super(CreateNetworkServer, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network server to the main configuration
        '''))
