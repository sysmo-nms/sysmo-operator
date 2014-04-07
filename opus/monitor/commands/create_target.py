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
    QPushButton
)

import nocapi


class Wizard(QWizard):
    NetElement  = 11
    NetService  = 21
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        self._configType = None
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        page1   = ChooseType(self)
        page2   = CreateNetworkElement(self)
        page3   = CreateNetworkServer(self)

        self.setPage(1,  page1)
        self.setPage(11, page2)
        self.setPage(21, page3)

        self.show()


class ChooseType(QWizardPage):
    def __init__(self, parent=None):
        super(ChooseType, self).__init__(parent)
        self._configType = Wizard.NetElement
        chooseTypeLayout    = QVBoxLayout(self)
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

        chooseTypeLayout.addWidget(typeNetElement)
        chooseTypeLayout.addWidget(typeNetService)
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
        layout = QFormLayout(self)
        checkGroup = QButtonGroup(self)
        checkGroup.setExclusive(True)

        ipLab = QLabel(self.tr('Ip address'), self)
        self.ipLine = QLineEdit(self)
        tempLab = QLabel(self.tr('Template'), self)
        self.tempBox = QComboBox(self)
        self.tempBox.addItem('Standard SNMP')
        layout.insertRow(0, ipLab,      self.ipLine)
        layout.insertRow(1, tempLab,    self.tempBox)

        checkV2     = QCheckBox(self)
        checkV2.setText(self.tr('SNMP v2'))
        checkV2.clicked.connect(self._setV2Conf)
        checkGroup.addButton(checkV2, CreateNetworkElement.V2)

        layout.insertRow(2, checkV2)

        self.rLab    = QLabel(self.tr('Read community:'), self)
        self.rLine   = QLineEdit(self)
        self.wLab    = QLabel(self.tr('Write community:'), self)
        self.wLine   = QLineEdit(self)
        layout.insertRow(3, self.rLab, self.rLine)
        layout.insertRow(4, self.wLab, self.wLine)

        checkV3     = QCheckBox(self)
        checkV3.setText(self.tr('SNMP v3'))
        checkV3.clicked.connect(self._setV3Conf)
        checkGroup.addButton(checkV3, CreateNetworkElement.V3)

        layout.insertRow(5, checkV3)

        self.lab1 = QLabel('lkj', self)
        self.lab2 = QLabel('lkj', self)
        self.lab3 = QLabel('lkj', self)
        self.line1 = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line3 = QLineEdit(self)
        layout.insertRow(6, self.lab1, self.line1)
        layout.insertRow(7, self.lab2, self.line2)
        layout.insertRow(8, self.lab3, self.line3)

        self.setLayout(layout)
        self._allDisabled()
        self.setFinalPage(True)
        self.setCommitPage(True)

    def _allDisabled(self):
        self.lab1.setDisabled(True)
        self.lab2.setDisabled(True)
        self.lab3.setDisabled(True)
        self.line1.setDisabled(True)
        self.line2.setDisabled(True)
        self.line3.setDisabled(True)
        self.rLab.setDisabled(True)
        self.wLab.setDisabled(True)
        self.rLine.setDisabled(True)
        self.wLine.setDisabled(True)

    def _setV2Conf(self):
        self.lab1.setDisabled(True)
        self.lab2.setDisabled(True)
        self.lab3.setDisabled(True)
        self.line1.setDisabled(True)
        self.line2.setDisabled(True)
        self.line3.setDisabled(True)
        self.rLab.setDisabled(False)
        self.wLab.setDisabled(False)
        self.rLine.setDisabled(False)
        self.wLine.setDisabled(False)

    def _setV3Conf(self):
        self.lab1.setDisabled(False)
        self.lab2.setDisabled(False)
        self.lab3.setDisabled(False)
        self.line1.setDisabled(False)
        self.line2.setDisabled(False)
        self.line3.setDisabled(False)
        self.rLab.setDisabled(True)
        self.wLab.setDisabled(True)
        self.rLine.setDisabled(True)
        self.wLine.setDisabled(True)

    def nextId(self):
        return -1


class CreateNetworkServer(QWizardPage):
    def __init__(self, parent=None):
        super(CreateNetworkServer, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Fill the form and add a network server to the main configuration
        '''))
