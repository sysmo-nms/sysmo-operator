from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton
from sysmo_widgets import NFrameContainer, NGridContainer, NInfoButton, NGrid, NFrame
from monitor.gui.tree.tree_view import ProbesTreeview
from monitor.dialogs.new_target import NewTargetDialog
import sysmapi


class ProbesTree(NFrame):
    def __init__(self, parent):
        super(ProbesTree, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self._grid = NGrid(self)
        self._probesActions     = ElementsActions(self)
        self._probesTreeview    = ProbesTreeview(self)
        self._connectControls()
        self._grid.addWidget(self._probesActions,   0,0)
        self._grid.addWidget(self._probesTreeview,  1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

    def _connectControls(self):
        self._probesActions.line.textChanged.connect(
            self._probesTreeview.filterThis
        )

class ElementsActions(NFrameContainer):
    def __init__(self, parent):
        super(ElementsActions, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)

        self.line = QLineEdit(self)
        self.line.setPlaceholderText('Filter')
        #self._line.textChanged.connect(self._lineChanged)

        #self.createMenu = QMenu(self)
        create = QPushButton(self)
        create.setFixedWidth(30)
        create.setIcon(QIcon(sysmapi.nGetPixmap('list-add')))
        create.setContentsMargins(0,0,0,0)
        #create.setMenu(NewTargetDialog(self))
        create.clicked.connect(self._launchWizard)
        #createAction = QWidgetAction(self)
        #createAction.setDefaultWidget(ElementsAdd(self))
        #self.createMenu.addAction(createAction)
        #create.setMenu(self.createMenu)
        #create.clicked.connect(self._createTargetWizard)

        clear = QPushButton(self)
        clear.setFixedWidth(30)
        clear.setIcon(QIcon(sysmapi.nGetPixmap('edit-clear')))
        clear.clicked.connect(self.line.clear)

        info = NInfoButton(self)

        grid.addWidget(create,      0,0)
        grid.addWidget(clear,       0,1)
        grid.addWidget(self.line,  0,2)
        grid.addWidget(info,        0,4)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)
        grid.setColumnStretch(3,3)
        grid.setColumnStretch(4,0)
        self.setLayout(grid)

    def _launchWizard(self):
        wizard = NewTargetDialog(self)
        wizard.show()
