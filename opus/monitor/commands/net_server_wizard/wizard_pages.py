from functools      import partial
from PySide.QtGui   import (
    QMenu,
    QWizardPage,
    QCheckBox,
    QFrame,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QGroupBox,
    QMessageBox,
    QRegExpValidator,
    QIntValidator
)
from PySide.QtCore import Qt, QPoint, QRegExp

from noctopus_widgets import (
    NGrid,
    NFrame,
    NGridContainer,
    NFrameContainer,
    Nipv4Validator
)

import nocapi
import opus.monitor.api as monapi
import opus.monitor.commands.wizards
import supercast.main   as supercast

class Page1(QWizardPage):
    IP_V4    = 0
    IP_V6    = 1
    NAME_MANUAL  = 0
    NAME_DYNAMIC = 1
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('Create a network server target'))
        self.setSubTitle(self.tr('''
            Define address, name and services for the target. 
        '''))
        self.setFinalPage(True)

        tempFrame   = NFrame(self)
        tempLayout  = NGrid(tempFrame)
        tempLayout.setContentsMargins(5,10,5,5)
        tempLayout.setVerticalSpacing(20)
        tempLayout.setRowStretch(1,0)
        tempFrame.setLayout(tempLayout)

        self._ipButton  = QComboBox(self)
        self._ipButton.insertItem(self.IP_V4, 'IP version 4')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6')
        self._ipLine    = QLineEdit(self)
        self._ipLine.setValidator(Nipv4Validator(self))

        self._nameButton = QComboBox(self)
        self._nameButton.insertItem(self.NAME_MANUAL,  'Manual name')
        self._nameButton.insertItem(self.NAME_DYNAMIC, 'Dynamic DNS name')
        self._nameLine  = QLineEdit(self)

        self.registerField('server_ip_version', self._ipButton)
        self.registerField('server_ip*',        self._ipLine)
        #self.registerField('server_ip',        self._ipLine)
        self.registerField('server_name_type',  self._nameButton)
        #self.registerField('server_name*',      self._nameLine)
        self.registerField('server_name',      self._nameLine)


        #########################
        # treeview probes begin #
        #########################
        probeFrame  = QGroupBox(self)
        probeFrame.setTitle(self.tr('Configure services checks'))
        probeLay    = NGrid(probeFrame)
        probeLay.setVerticalSpacing(5)

        self._checkDefs = monapi.getCheckInfos()
        checkMenu = QMenu(self)
        for key in self._checkDefs.keys():
            action = checkMenu.addAction(key)
            action.triggered.connect(partial(self._openProbeConfig, key))

        checkAddButton = QPushButton(self)
        #checkAddButton.setText(self.tr('Add a new probe'))
        checkAddButton.setIcon(nocapi.nGetIcon('list-add'))
        checkAddButton.setMenu(checkMenu)

        self._checksTree = QTreeWidget(self)

        probeLay.addWidget(checkAddButton,   0,0,1,1)
        probeLay.addWidget(self._checksTree, 1,0,1,2)
        probeLay.setColumnStretch(0,0)
        probeLay.setColumnStretch(1,1)
        probeLay.setRowStretch(0,1)
        probeLay.setRowStretch(1,1)
        probeFrame.setLayout(probeLay)
        #########################
        # treeview probes end   #
        #########################

        tempLayout.addWidget(self._ipButton,    0,0)
        tempLayout.addWidget(self._ipLine,      0,1)
        tempLayout.addWidget(self._nameButton,  1,0)
        tempLayout.addWidget(self._nameLine,    1,1)
        tempLayout.addWidget(probeFrame,        2,0,1,2)
        #tempLayout.addWidget(self._checksTree,  2,1,2,1)

        layout = NGridContainer(self)
        layout.addWidget(tempFrame, 0,0)
        
        self.setLayout(layout)

    def _openProbeConfig(self, key):
        wiz = opus.monitor.commands.wizards.ProbeWizard(
            self._checkDefs, key, self, self._ipLine.text()
        )
        wiz.show()

    def validatePage(self):
        print "validate"
        return False

    def nextId(self):
        return -1
