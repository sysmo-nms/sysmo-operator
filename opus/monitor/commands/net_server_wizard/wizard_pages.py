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
    QMessageBox
)
from PySide.QtCore import Qt

from noctopus_widgets import NGrid, NFrame, NGridContainer, NFrameContainer
import nocapi
import opus.monitor.api as monapi
from opus.monitor.commands.configure_probe import ProbeForm
import supercast.main   as supercast

class Page1(QWizardPage):
    IP_V4    = 0
    IP_V6    = 1
    NAME_MANUAL  = 0
    NAME_DYNAMIC = 1
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Define the address ip of the server.
        '''))
        self.setFinalPage(False)

        tempFrame   = NFrame(self)
        tempLayout  = NGrid(tempFrame)
        tempLayout.setVerticalSpacing(20)
        tempLayout.setRowStretch(1,0)
        tempFrame.setLayout(tempLayout)

        self._ipButton  = QComboBox(self)
        self._ipButton.insertItem(self.IP_V4, 'IP version 4')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6')
        self._ipLine    = QLineEdit(self)
        #self._ipLine.setInputMask('000.000.000.000')

        self._nameButton = QComboBox(self)
        self._nameButton.insertItem(self.NAME_MANUAL,  'Manual name')
        self._nameButton.insertItem(self.NAME_DYNAMIC, 'Dynamic DNS name')
        self._nameLine  = QLineEdit(self)

        self.registerField('server_ip_version', self._ipButton)
        #self.registerField('server_ip*',        self._ipLine)
        self.registerField('server_ip',        self._ipLine)
        self.registerField('server_name_type',  self._nameButton)
        #self.registerField('server_name*',      self._nameLine)
        self.registerField('server_name',      self._nameLine)

        tempLayout.addWidget(self._ipButton,    0,0)
        tempLayout.addWidget(self._ipLine,      0,1)
        tempLayout.addWidget(self._nameButton,  1,0)
        tempLayout.addWidget(self._nameLine,    1,1)

        layout = NGridContainer(self)
        layout.addWidget(tempFrame, 0,0)
        
        self.setLayout(layout)

    def nextId(self):
        return 22

class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setTitle(self.tr('Edit check configuration'))
        self.setSubTitle(self.tr('''
            Define what checks you want to execute on this server.
        '''))
        self.setFinalPage(False)

        self._checkDefs = monapi.getCheckInfos()
        checkMenu = QMenu(self)
        for key in self._checkDefs.keys():
            action = checkMenu.addAction(key)
            action.triggered.connect(partial(self._openProbeConfig, key))

        checksAddButton = QPushButton(self)
        checksAddButton.setText(self.tr('Add a new probe'))
        checksAddButton.setIcon(nocapi.nGetIcon('list-add'))
        checksAddButton.setMenu(checkMenu)


        checksTreeView = QTreeWidget(self)

        layout = NGrid(self)
        layout.addWidget(checksAddButton, 0,0,1,2)
        layout.addWidget(checksTreeView,  1,0,1,2)
        layout.setColumnStretch(0,0)
        layout.setColumnStretch(1,1)


        self.setLayout(layout)

    def _openProbeConfig(self, key):
        dial = ProbeForm(self._checkDefs, key, self)
        ret = dial.show()

    def receiveProbeConfig(self, config):
        print "receive probe config"

    def nextId(self):
        return 23










class Page3(QWizardPage):
    IP_V4    = 0
    IP_V6    = 1
    NAME_MANUAL  = 0
    NAME_DYNAMIC = 1
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Define the address ip of the server.
        '''))
        layout = NGrid(self)
        self.setFinalPage(False)
        
        self._ipLine    = QLineEdit(self)
        self._ipButton  = QComboBox(self)
        self._ipButton.insertItem(self.IP_V4, 'aaaaaaarqqqqqqqq')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6')

        layout.addWidget(self._ipButton,    1,1)
        layout.addWidget(self._ipLine,      1,2)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,0)
        layout.setRowStretch(2,3)
        layout.setContentsMargins(100,0,100,0)
        self.setLayout(layout)
