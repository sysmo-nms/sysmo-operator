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
    def __init__(self, defs, key, parent):
        super(ProbeWizard, self).__init__(parent)
        #self.setFixedWidth(800)
        self.setModal(True)
        ppage1 = ProbeElement.Page1(defs, key, self)
        ppage2 = ProbeElement.Page2(self)
        self.setPage(1, ppage1)
        self.setPage(2, ppage2)
        self.setStartId(1)
        self.show()


class TargetWizard(QWizard):
    NetElement  = 11
    NetService  = 21
    def __init__(self, parent=None):
        super(TargetWizard, self).__init__(parent)
        self.setModal(True)
        self._configType = None
        pix = nocapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.HaveHelpButton,          True)
        self.setOption(QWizard.HelpButtonOnRight,       False)

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
        self._configType = TargetWizard.NetElement
        self._parent.next()

    def _startNetService(self):
        self._configType = TargetWizard.NetService
        self._parent.next()

    def nextId(self):
        return self._configType
