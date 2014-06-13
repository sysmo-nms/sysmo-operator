from    PySide.QtGui    import (
    QLineEdit,
    QPushButton,
    QCommandLinkButton,
    QWidgetAction,
    QMenu
)

from    noctopus_widgets        import (
    NFrameContainer,
    NGridContainer,
    NInfoButton,
    NGrid
)

from    opus.monitor.commands.wizards import (
    NetworkElementWizard,
    NetworkServerWizard
)
import nocapi

class ProbesActions(NFrameContainer):
    def __init__(self, parent):
        super(ProbesActions, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)

        self._line = QLineEdit(self)
        self._line.setPlaceholderText('Filter')
        self._line.textChanged.connect(self._lineChanged)

        self.createMenu = QMenu(self)
        create   = QPushButton(self)
        create.setFixedWidth(32)
        create.setIcon(nocapi.nGetIcon('list-add'))
        create.setContentsMargins(0,0,0,0)
        createAction = QWidgetAction(self)
        createAction.setDefaultWidget(ProbesAdd(self))
        self.createMenu.addAction(createAction)
        create.setMenu(self.createMenu)
        #create.clicked.connect(self._createTargetWizard)

        clear = QPushButton(self)
        clear.setFixedWidth(32)
        clear.setIcon(nocapi.nGetIcon('edit-clear'))
        clear.clicked.connect(self._line.clear)

        info = NInfoButton(self)

        grid.addWidget(create,      0,0)
        grid.addWidget(clear,       0,1)
        grid.addWidget(self._line,  0,2)
        grid.addWidget(info,        0,3)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)
        grid.setColumnStretch(3,0)
        self.setLayout(grid)

    def _lineChanged(self):
        text = self._line.text()
        print text

class ProbesAdd(NFrameContainer):
    def __init__(self, parent):
        super(ProbesAdd, self).__init__(parent)
        self._createMenu = parent.createMenu
        self.setFixedWidth(300)
        grid = NGrid(self)
        grid.setVerticalSpacing(0)
        addNetServerButton = QCommandLinkButton(
            self.tr('Add a network server'),
            self.tr('A network server offer services like HTTP, IMAP...'),
            self
        )
        addNetElementButton = QCommandLinkButton(
            self.tr('Add a network element'),
            self.tr('A network element must responde to SNMP and implement the MIB2 tree.'),
            self
        )
        addNetServiceButton = QCommandLinkButton(
            self.tr('Add a service'),
            self.tr('A service offer user functionnality depending on multiple network server services or elements'),
            self
        )
        addNetServiceButton.setDisabled(True)

        addNetServerButton.setIcon(nocapi.nGetIcon('applications-system'))
        addNetElementButton.setIcon(nocapi.nGetIcon('network-wired'))
        addNetServiceButton.setIcon(nocapi.nGetIcon('system-users'))

        addNetServerButton.clicked.connect(self._addServer)
        addNetElementButton.clicked.connect(self._addElement)
        addNetServiceButton.clicked.connect(self._addService)

        grid.addWidget(addNetServerButton,  0,0)
        grid.addWidget(addNetElementButton, 1,0)
        grid.addWidget(addNetServiceButton, 2,0)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)
        self.setLayout(grid)

    def _addServer(self):
        self._createMenu.hide()
        wizard = NetworkServerWizard(self)
        wizard.show()

    def _addElement(self):
        self._createMenu.hide()
        wizard = NetworkElementWizard(self)
        wizard.show()

    def _addService(self):
        self._createMenu.hide()






