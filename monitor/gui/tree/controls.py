from    PyQt5.QtGui    import QIcon
from    PyQt5.QtWidgets    import (
    QLineEdit,
    QPushButton,
    QCommandLinkButton,
    QWidgetAction,
    QMenu
)

from    sysmo_widgets        import (
    NFrameContainer,
    NGridContainer,
    NInfoButton,
    NGrid
)

from    monitor.commands.target_utils import NewTargetDialog

import sysmapi

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
