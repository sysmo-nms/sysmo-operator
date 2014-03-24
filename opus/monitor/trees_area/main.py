from    PySide.QtCore   import *
from    PySide.QtGui    import *
from    noctopus_widgets import NFrame
#from    MonitorProxyEvents   import ChannelHandler
#from    DashboardTree   import *
#import    MonitorDashboardArea
#from    NewTargetForm   import  AddTargetWizard
#from    CommonWidgets   import  *
#import  TkorderIcons


class TreeContainer(NFrame):
    
    " the left tree area. Emit user clics events"

    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self

        QLabel('hello',self)
#         self.trackerMain  = parent
# 
#         self.commands   = Commands(self)
#         self.searchBar  = MonitorTreeSearch(self)
# 
#         self.treeview   = MonitorTreeView(self)
#         self.dashboardList = DashboardTreeView(self)
#         self.vServices  = VirtualServices(self)
#         self.tabs       = QTabWidget(self)
#         self.tabs.addTab(self.dashboardList,    'Dashboards')
#         self.tabs.addTab(self.vServices,        'Services')
#         self.tabs.addTab(self.treeview,         'Probes')
#         self.tabs.addTab(QLabel('elements', self), 'SNMP Elements')
#         self.tabs.setCurrentWidget(self.treeview)
# 
#         self.info       = MonitorTreeAreaInfo(self)
#         self.osmView    = OSMView(self)
#         self.osmView.setFrameShape(QFrame.StyledPanel)
#         self.osmView.setFrameShadow(QFrame.Raised)
#         self.osmView.setBrowsable(False)
# 
#         self.osmView.hide()
#         self.osmView.setFixedHeight(300)
# 
#         self.grid = QGridLayout(self)
#         self.grid.setContentsMargins(0,0,0,0)
#         self.grid.setHorizontalSpacing(0)
#         self.grid.setVerticalSpacing(5)
#         self.setMinimumWidth(350)
#         
#         self.grid.addWidget(self.commands,           1, 0)
#         self.grid.addWidget(self.searchBar,          2, 0)
#         self.grid.addWidget(self.tabs,               3, 0)
#         self.grid.addWidget(self.info,               4, 0)
# 
#         self.grid.setRowStretch(0,0)
#         self.grid.setRowStretch(1,0)
#         self.grid.setRowStretch(2,0)
#         self.grid.setRowStretch(3,1)
#         self.grid.setRowStretch(4,0)
# 
#         self.setLayout(self.grid)
# 
#         self.viewMode = 'full'
#         self.setMaximumWidth(500)
# 
#     def setMinimalView(self, bol):
#         if bol == True and self.viewMode == 'full':
#             self.commands.hide()
#             self.grid.removeWidget(self.info)
#             self.info.hide()
#             self.osmView.show()
#             self.grid.addWidget(self.osmView, 4,0)
#             self.viewMode = 'minimal'
#         elif bol == False and self.viewMode == 'minimal':
#             self.commands.show()
#             self.grid.removeWidget(self.osmView)
#             self.osmView.hide()
#             self.info.show()
#             self.grid.addWidget(self.info, 4,0)
#             self.viewMode = 'full'
# 
# class VirtualServices(QTreeView):
#     def __init__(self, parent):
#         super(VirtualServices, self).__init__(parent)
#         self.setAnimated(True)
#         self.setFrameShape(QFrame.NoFrame)
#         self.setHeaderHidden(False)
# 
# class Commands(QFrame):
#     def __init__(self, parent):
#         super(Commands, self).__init__(parent)
#         grid = QGridLayout(self)
#         grid.setContentsMargins(0,0,0,0)
#         grid.setHorizontalSpacing(5)
#         grid.setVerticalSpacing(0)
#         self.addButton = QPushButton(TkorderIcons.get('list-add'), 'Add', self)
#         self.addButton.clicked.connect(self._launchWizard)
#         grid.addWidget(self.addButton, 0,0)
#         grid.setColumnStretch(0,0)
#         grid.setColumnStretch(1,1)
#         self.setLayout(grid)
# 
#     def _launchWizard(self):
#         wizard = AddTargetWizard(self)
# 
# 
# 
# 
# class MonitorTreeSearch(QFrame):
#     def __init__(self, parent):
#         super(MonitorTreeSearch, self).__init__(parent)
#         grid = QGridLayout(self)
#         grid.setContentsMargins(0,0,0,0)
#         grid.setHorizontalSpacing(5)
#         grid.setVerticalSpacing(0)
# 
#         self.line = QLineEdit(self)
#         self.line.setPlaceholderText('Filter')
#         self.line.textChanged.connect(self.lineTextUpdate)
# 
#         clear   = QPushButton(self)
#         clear.setIcon(TkorderIcons.get('edit-clear'))
#         clear.clicked.connect(self.line.clear)
# 
#         grid.addWidget(clear,   0,0)
#         grid.addWidget(self.line,    0,1)
# 
#         grid.setColumnStretch(0,0)
#         grid.setColumnStretch(1,1)
#         grid.setColumnStretch(2,0)
#         self.setLayout(grid)
# 
#     def lineTextUpdate(self):
#         text = self.line.text()
#         MonitorTreeView.singleton.filterThis(text)
# 
# 
# class MonitorTreeButtons(QToolBar):
#     def __init__(self, parent):
#         super(MonitorTreeButtons, self).__init__(parent)
#         self.addAction(TkorderIcons.get('applications-development'), 'Debug', self.hello())
# 
#     def hello(self): pass
# 
# class MonitorTreeAreaInfo(QTextEdit):
#     def __init__(self, parent):
#         super(MonitorTreeAreaInfo, self).__init__(parent)
#         # text document
#         dtext   = QTextDocument()
#         dtext.setMaximumBlockCount(500)
#         tformat = QTextCharFormat()
#         tformat.setFontPointSize(8.2)
# 
#         # QTextEdit config
#         self.setDocument(dtext)
#         self.setCurrentCharFormat(tformat)
#         self.setReadOnly(True)
#         #self.setStyleSheet(
#             #"QTextEdit { \
#                 #border-radius: 10px;\
#                 #background: #F9EE75 \
#             #}")
#         self.setFixedHeight(100)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setFrameShadow(QFrame.Raised)
# 
#         # signals to receive
#         sigDict = ChannelHandler.singleton.masterSignalsDict
#         sigDict['probeInfo'].signal.connect(self._informational)
#         sigDict['targetInfo'].signal.connect(self._informational)
#         sigDict['probeModInfo'].signal.connect(self._informational)
# 
#     def _informational(self, msg):
#         self.append(str(msg))
