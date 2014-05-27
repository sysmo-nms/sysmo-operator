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
        layout = NGrid(self)
        self.setFinalPage(False)
        
        self._ipLine    = QLineEdit(self)
        self._ipButton  = QComboBox(self)
        self._ipButton.insertItem(self.IP_V4, 'IP version 4')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6')

        layout.addWidget(self._ipButton,    1,1)
        layout.addWidget(self._ipLine,      1,2)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,0)
        layout.setRowStretch(2,3)
        layout.setContentsMargins(100,0,100,0)
        self.setLayout(layout)

    def nextId(self):
        return 22

class Page2(QWizardPage):
    IP_V4    = 0
    IP_V6    = 1
    NAME_MANUAL  = 0
    NAME_DYNAMIC = 1
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setTitle(self.tr('Create a network server'))
        self.setSubTitle(self.tr('''
            Define the address ip of the server.
        '''))
        layout = NGrid(self)
        self.setFinalPage(False)
        
        self._ipLine    = QLineEdit(self)
        self._ipButton  = QComboBox(self)
        self._ipButton.insertItem(self.IP_V4, 'qqqqqqqqqqqqqqqq')
        self._ipButton.insertItem(self.IP_V6, 'IP version 6')

        layout.addWidget(self._ipButton,    1,1)
        layout.addWidget(self._ipLine,      1,2)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,0)
        layout.setRowStretch(2,3)
        layout.setContentsMargins(100,0,100,0)
        self.setLayout(layout)

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

class PageX(QWizardPage):
    IP_V4    = 0
    IP_V6    = 1
    NAME_MANUAL  = 0
    NAME_DYNAMIC = 1
    def __init__(self, parent=None):
        super(PageX, self).__init__(parent)
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
        #print "send"
        #ret = supercast.send(
            #'query',
            #'getChecksInfo',
            #self.monitorReply
        #)
        return False

    def _assertCmd(self, a,b,c,d,e): return True

    def monitorReply(self, msg):
        print "get reply!!!!!!", msg
