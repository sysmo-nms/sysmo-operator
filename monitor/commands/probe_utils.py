from PyQt5.QtWidgets   import (
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
from PyQt5.QtCore import Qt

from sysmo_widgets import NGrid, NFrame, NGridContainer, NFrameContainer
import sysmapi
import monitor.api as monapi
import supercast.main   as supercast


import monitor.commands.net_element_wizard.wizard_pages  as NetElement
#import monitor.commands.net_server_wizard.wizard_pages   as SrvElement
import monitor.commands.probe_wizard.wizard_pages        as ProbeElement
import monitor.commands.user_actions_wizard.wizard_pages as UActionPages
import monitor.commands.properties as PropInfo

import monitor.commands.add_element_pages as AddElementPages
from monitor.commands.properties import SnmpConfigFrame


# OLD WIZARDS
class CreateProbeDialog(QWizard):
    def __init__(self, parent=None, element=None):
        super(CreateProbeDialog, self).__init__(parent)
        self.setModal(True)
        self.show()

class UserActionsWizard(QWizard):
    def __init__(self, parent=None, element=None):
        super(UserActionsWizard, self).__init__(parent)

        self.setModal(True)
        page1 = UActionPages.Page1(self, element)
        self.setPage(1, page1)
        self.setStartId(1)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.WatermarkPixmap, sysmapi.nGetPixmap('console'))
        self.setPixmap(QWizard.LogoPixmap,sysmapi.nGetPixmap('applications-system'))
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
        self.setPixmap(QWizard.WatermarkPixmap, sysmapi.nGetPixmap('radar'))
        self.setPixmap(QWizard.LogoPixmap,sysmapi.nGetPixmap('applications-system'))
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


class NetworkServerWizard(QWizard):
    def __init__(self, parent=None):
        super(NetworkServerWizard, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.WatermarkPixmap, sysmapi.nGetPixmap('server-bay'))

        self.setModal(True)
        pix = sysmapi.nGetPixmap('applications-system')
        self.setPixmap(QWizard.LogoPixmap, pix)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        npage1   = SrvElement.Page1(self)
        self.setPage(1, npage1)
        self.setStartId(1)
