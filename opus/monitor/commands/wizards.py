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
import opus.monitor.api as monapi
import supercast.main   as supercast

import opus.monitor.commands.net_element_wizard.wizard_pages as NetElement
import opus.monitor.commands.net_server_wizard.wizard_pages  as SrvElement
import opus.monitor.commands.probe_wizard.wizard_pages       as ProbeElement


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
        # page2 use QWizard.registerField
        # self.page2_config = None 
        self.show()

    def validateConfig(self):
        checkDef = dict()
        checkDef['def']     = self.page1_config
        checkDef['display_name'] = self.field('p2_display_name')
        checkDef['step']    = self.field('p2_check_step')
        checkDef['alert']   = self.page3_config

        descr   = self.field('p2_description')
        if descr == None:
            checkDef['descr'] = ""
        else:
            checkDef['descr'] = descr

        self._callback(checkDef)


class TargetWizard(QWizard):
    NetElement  = 11
    NetServer   = 21
    NetService  = 31
    def __init__(self, parent=None):
        super(TargetWizard, self).__init__(parent)
        self.setModal(True)
        self._configType = None
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)

        self.setButtonText(QWizard.CancelButton, self.tr("&Close"))
        self.setButtonText(QWizard.FinishButton, self.tr("&Apply"))

        page1   = ChooseType(self)
        self.setPage(1,  page1)

        npage1   = NetElement.Page1(self)
        self.setPage(11, npage1)

        spage1   = SrvElement.Page1(self)
        self.setPage(21, spage1)

        self.setStartId(1)

        self.show()

class NewProbeWizard(QWizard):
    def __init__(self, parent=None):
        super(NewProbeWizard, self).__init__(parent)
        self.setPage(1, SrvElement.Page3(self))
        self.setStartId(1)
        self.show()

class ChooseType(QWizardPage):
    def __init__(self, parent=None):
        super(ChooseType, self).__init__(parent)
        self._configType = TargetWizard.NetElement
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
        '''))
        typeNetElement.clicked.connect(self._startNetElement)

        typeNetServer      = QCommandLinkButton(self)
        typeNetServer.setMaximumHeight(200)
        typeNetServer.setText('Network server')
        typeNetServer.setDescription(self.tr('''
            Create a network server target, and get live status of services.
            This wizard will help you to create a network server target.
        '''))
        typeNetServer.clicked.connect(self._startNetServer)

        typeNetService      = QCommandLinkButton(self)
        typeNetService.setMaximumHeight(200)
        typeNetService.setText('Network service')
        typeNetService.setDescription(self.tr('''
            Create a network server target, and get live status of services.
            This wizard will help you to create a network server target.
        '''))
        typeNetService.clicked.connect(self._startNetService)

        chooseTypeLayout.addWidget(typeNetElement, 0,0)
        chooseTypeLayout.addWidget(typeNetServer,  1,0)
        chooseTypeLayout.addWidget(typeNetService, 2,0)
        chooseTypeLayout.setRowStretch(0,1)
        chooseTypeLayout.setRowStretch(1,1)
        chooseTypeLayout.setRowStretch(2,1)

        self.setLayout(chooseTypeLayout)

    def _startNetElement(self):
        self._configType = TargetWizard.NetElement
        self._parent.next()

    def _startNetServer(self):
        self._configType = TargetWizard.NetServer
        self._parent.next()

    def _startNetService(self): pass

    def nextId(self):
        return self._configType
