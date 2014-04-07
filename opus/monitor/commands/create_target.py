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
    QListWidget
)

from noctopus_widgets import NGrid, NFrame
import nocapi


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
        typeNetElement.setText('Network element')
        typeNetElement.setDescription(self.tr('''
            Create a network element target, and get live status and
            performances graphics
        '''))
        typeNetElement.clicked.connect(self._startNetElement)

        typeNetService      = QCommandLinkButton(self)
        typeNetService.setText('Network server')
        typeNetService.setDescription(self.tr('''
            Create a network server target, and get live status of services.
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
        layout.addWidget(self._initTemplates(),         0,0,1,2)
        layout.addWidget(self._initPropertiesFrame(),   1,0,1,1)
        layout.addWidget(self._initSnmpFrame(),         1,1,1,1)
        layout.addWidget(self._initProbesFrame(),       2,0,1,2)
        self.setLayout(layout)

    def _initTemplates(self):
        tempFrame   = NFrame(self)
        tempLayout  = NGrid(tempFrame)
        tempFrame.setLayout(tempLayout)
        tempLayout.addWidget(QLabel('Use a template', tempFrame),   0,0)
        tempLayout.addWidget(QComboBox(tempFrame),                  0,1)
        lab = QLabel('''<p>
            The view classes that inherit PySide.QtGui.QAbstractItemView only need to implement their own view-specific functionality, such as drawing items, returning the geometry of items, finding items, etc</p>
        ''')
        lab.setWordWrap(True)
        tempLayout.addWidget(lab, 1,0,1,2)
        tempLayout.setColumnStretch(0,0)
        tempLayout.setColumnStretch(1,1)
        return tempFrame

    def _initPropertiesFrame(self):
        propFrame = QGroupBox(self)
        propFrame.setTitle(self.tr("&Properties"))
        propLayout = QFormLayout(propFrame)
        propFrame.setLayout(propLayout)

        ipLabel = QLabel(self.tr("Ip address:"), propFrame)
        ipLine  = QLineEdit(propFrame)

        hnLabel = QLabel(self.tr("Hostname:"), propFrame)
        hnLine  = QLineEdit(propFrame)

        custom      = QGroupBox(propFrame)
        custom.setTitle(self.tr("User properties"))
        customGrid  = NGrid(custom)
        customGrid.addWidget(QListWidget(custom),   1,0,1,2)
        custom.setLayout(customGrid)

        propLayout.insertRow(0, ipLabel, ipLine)
        propLayout.insertRow(1, hnLabel, hnLine)
        propLayout.insertRow(2, custom)

        return propFrame

    def _initSnmpFrame(self):
        snmpFrame = QGroupBox(self)
        snmpFrame.setTitle(self.tr("&SNMP configuration"))
        snmpLayout = QFormLayout(snmpFrame)
        snmpFrame.setLayout(snmpLayout)

        snmpLayout.insertRow(0, self.tr('RO community'), QLineEdit(snmpFrame))
        snmpLayout.insertRow(1, self.tr('RW community'), QLineEdit(snmpFrame))
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
        print "validate"
        return False

        

#         layout = QFormLayout(self)
#         checkGroup = QButtonGroup(self)
#         checkGroup.setExclusive(True)
# 
#         ipLab = QLabel(self.tr('Ip address'), self)
#         self.ipLine = QLineEdit(self)
#         tempLab = QLabel(self.tr('Template'), self)
#         self.tempBox = QComboBox(self)
#         self.tempBox.addItem('Standard SNMP')
#         layout.insertRow(0, ipLab,      self.ipLine)
#         layout.insertRow(1, tempLab,    self.tempBox)
# 
#         checkV2     = QCheckBox(self)
#         checkV2.setText(self.tr('SNMP v2'))
#         checkV2.clicked.connect(self._setV2Conf)
#         checkGroup.addButton(checkV2, CreateNetworkElement.V2)
# 
#         layout.insertRow(2, checkV2)
# 
#         self.rLab    = QLabel(self.tr('Read community:'), self)
#         self.rLine   = QLineEdit(self)
#         self.wLab    = QLabel(self.tr('Write community:'), self)
#         self.wLine   = QLineEdit(self)
#         layout.insertRow(3, self.rLab, self.rLine)
#         layout.insertRow(4, self.wLab, self.wLine)
# 
#         checkV3     = QCheckBox(self)
#         checkV3.setText(self.tr('SNMP v3'))
#         checkV3.clicked.connect(self._setV3Conf)
#         checkGroup.addButton(checkV3, CreateNetworkElement.V3)
# 
#         layout.insertRow(5, checkV3)
# 
#         self.lab1 = QLabel('lkj', self)
#         self.lab2 = QLabel('lkj', self)
#         self.lab3 = QLabel('lkj', self)
#         self.line1 = QLineEdit(self)
#         self.line2 = QLineEdit(self)
#         self.line3 = QLineEdit(self)
#         layout.insertRow(6, self.lab1, self.line1)
#         layout.insertRow(7, self.lab2, self.line2)
#         layout.insertRow(8, self.lab3, self.line3)
# 
#         self.setLayout(layout)
#         self._allDisabled()
#         self.setFinalPage(True)
#         self.setCommitPage(True)
# 
#     def _allDisabled(self):
#         self.lab1.setDisabled(True)
#         self.lab2.setDisabled(True)
#         self.lab3.setDisabled(True)
#         self.line1.setDisabled(True)
#         self.line2.setDisabled(True)
#         self.line3.setDisabled(True)
#         self.rLab.setDisabled(True)
#         self.wLab.setDisabled(True)
#         self.rLine.setDisabled(True)
#         self.wLine.setDisabled(True)
# 
#     def _setV2Conf(self):
#         self.lab1.setDisabled(True)
#         self.lab2.setDisabled(True)
#         self.lab3.setDisabled(True)
#         self.line1.setDisabled(True)
#         self.line2.setDisabled(True)
#         self.line3.setDisabled(True)
#         self.rLab.setDisabled(False)
#         self.wLab.setDisabled(False)
#         self.rLine.setDisabled(False)
#         self.wLine.setDisabled(False)
# 
#     def _setV3Conf(self):
#         self.lab1.setDisabled(False)
#         self.lab2.setDisabled(False)
#         self.lab3.setDisabled(False)
#         self.line1.setDisabled(False)
#         self.line2.setDisabled(False)
#         self.line3.setDisabled(False)
#         self.rLab.setDisabled(True)
#         self.wLab.setDisabled(True)
#         self.rLine.setDisabled(True)
#         self.wLine.setDisabled(True)
# 


class CreateNetworkServer(QWizardPage):
    def __init__(self, parent=None):
        super(CreateNetworkServer, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network server to the main configuration
        '''))
