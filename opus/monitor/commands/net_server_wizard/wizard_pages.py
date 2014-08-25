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
    NIpv4Validator
)

import copy
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
        self._ipButton.setFocusPolicy(Qt.ClickFocus)
        self._ipLine    = QLineEdit(self)

        self._nameButton = QComboBox(self)
        self._nameButton.insertItem(self.NAME_MANUAL,  'Manual name')
        self._nameButton.insertItem(self.NAME_DYNAMIC, 'Dynamic DNS name')
        self._nameButton.setFocusPolicy(Qt.ClickFocus)
        self._nameLine  = QLineEdit(self)

        self.registerField('server_ip_version', self._ipButton)
        self.registerField('server_ip*',        self._ipLine)
        self.registerField('server_name_type',  self._nameButton)
        self.registerField('server_name*',      self._nameLine)

        self._checkConfigs = list()


        #########################
        # treeview probes begin #
        #########################
        self.probeFrame  = QGroupBox(self)
        self.probeFrame.setTitle(self.tr('Configure services checks'))
        probeLay    = NGrid(self.probeFrame)
        probeLay.setVerticalSpacing(5)

        self._checkDefs = monapi.getCheckInfos()
        checkMenu = QMenu(self)
        for key in self._checkDefs.keys():
            action = checkMenu.addAction(key)
            action.triggered.connect(partial(self._openProbeConfig, key))

        checkAddButton = QPushButton(self)
        checkAddButton.setIcon(nocapi.nGetIcon('list-add'))
        checkAddButton.setMenu(checkMenu)

        self._checksTree = QTreeWidget(self)
        self._checksTree.setColumnCount(2)
        self._checksTree.setHeaderLabels(["Checks", "Description"])

        probeLay.addWidget(checkAddButton,   0,0,1,1)
        probeLay.addWidget(self._checksTree, 1,0,1,2)
        probeLay.setColumnStretch(0,0)
        probeLay.setColumnStretch(1,1)
        probeLay.setRowStretch(0,1)
        probeLay.setRowStretch(1,1)
        self.probeFrame.setLayout(probeLay)
        #########################
        # treeview probes end   #
        #########################

        tempLayout.addWidget(self._ipButton,    0,0)
        tempLayout.addWidget(self._ipLine,      0,1)
        tempLayout.addWidget(self._nameButton,  1,0)
        tempLayout.addWidget(self._nameLine,    1,1)
        tempLayout.addWidget(self.probeFrame,        2,0,1,2)

        layout = NGridContainer(self)
        layout.addWidget(tempFrame, 0,0)
        
        self.completeChanged.connect(self._formComplete)
        self.setLayout(layout)

    def initializePage(self):
        self._formComplete()

    def _formComplete(self):
        if self.isComplete() == True:
            self.probeFrame.setDisabled(False)
        else:
            self.probeFrame.setDisabled(True)
            
    def _probeConfigCallback(self, probeConfig):
        self._checkConfigs.append(probeConfig)
        name        = probeConfig['display_name']
        descr       = probeConfig['descr']
        self._checksTree.addTopLevelItem(QTreeWidgetItem(None, [name, descr]))

    def _openProbeConfig(self, key):
        wiz = opus.monitor.commands.wizards.ProbeWizard(
            self._checkDefs, key, self, 
            self._probeConfigCallback, self._ipLine.text()
        )
        wiz.show()

    def validatePage(self):
        self._createTarget()
        return False



    def _createTarget(self):
        supercast.send(
            'monitorCreateTarget',
            (
                self._ipLine.text(),
                (["admin"], ["admin"]),
                self._nameLine.text(),
                "undefined",
                "undefined",
                "undefined"
            ),
            self.createTargetCallback
        )

    def createTargetCallback(self, msg):
        if msg['value']['status'] == True:
            self._targetName = msg['value']['info']
            self._processProbes = copy.deepcopy(self._checkConfigs)
            self._createProbes()

    def _createProbes(self):
        if len(self._processProbes) != 0:
            pconf = self._processProbes.pop()

            for i in range(len(pconf['def']['flags'])):
                f = pconf['def']['flags'][i]
                fl,ar = f
                if fl == 'timeout':
                    timeout = ar
                    break

            supercast.send(
                'monitorCreateSimpleProbe',
                (
                    self._targetName,
                    pconf['display_name'],
                    pconf['descr'],
                    (["admin"],["admin"]),
                    "simple",
                    timeout,
                    pconf['step'],
                    pconf['def']['flags'],
                    pconf['exe']
                ),
                self.createProbesCallback
            )
    
    def createProbesCallback(self, msg):
        print "next pass ", msg
        if msg['value']['status'] == True:
            self._createProbes()

    def nextId(self):
        return -1
