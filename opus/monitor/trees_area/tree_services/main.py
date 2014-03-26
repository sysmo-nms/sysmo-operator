from    PySide.QtGui    import (
    QTreeView,
    QFrame,
    QLineEdit,
    QPushButton
)

from noctopus_widgets   import (
    NFrame,
    NFrameContainer,
    NGridContainer,
    NGrid
)

import nocapi


class ServicesTree(NFrame):
    def __init__(self, parent):
        super(ServicesTree, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self._grid = NGrid(self)
        self._servicesActions  = ServicesActions(self)
        self._servicesTreeview = ServicesTreeview(self)
        self._grid.addWidget(self._servicesActions,  0,0)
        self._grid.addWidget(self._servicesTreeview, 1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

class ServicesTreeview(QTreeView):
    def __init__(self, parent):
        super(ServicesTreeview, self).__init__(parent)
        self.setAnimated(True)
        self.setHeaderHidden(False)
        self.setObjectName('serviceTree')
        self.setStyleSheet('''QFrame#serviceTree {
            background-image: url(./graphics/hover_info_files.png);
            background-repeat: no-repeat;
            background-color: %s;
            background-attachment: fixed;
            background-position: bottom right}''' % nocapi.nGetRgb('Base'))

class ServicesActions(NFrameContainer):
    def __init__(self, parent):
        super(ServicesActions, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)

        self._line = QLineEdit(self)
        self._line.setPlaceholderText('Filter')
        self._line.textChanged.connect(self._lineChanged)

        add   = QPushButton(self)
        add.setIcon(nocapi.nGetIcon('list-add'))

        clear = QPushButton(self)
        clear.setIcon(nocapi.nGetIcon('edit-clear'))
        clear.clicked.connect(self._line.clear)

        grid.addWidget(add,         0,0)
        grid.addWidget(clear,       0,1)
        grid.addWidget(self._line,  0,2)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)
        self.setLayout(grid)

    def _lineChanged(self):
        text = self._line.text()
        print text
        #MonitorTreeview.singleton.filterThis(text)
