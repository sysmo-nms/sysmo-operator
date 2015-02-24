from    PyQt5.QtGui    import QIcon
from    PyQt5.QtWidgets    import (
    QLineEdit,
    QPushButton
)

from    sysmo_widgets        import (
    NFrameContainer,
    NGridContainer
)

import sysmapi

class DashActions(NFrameContainer):
    def __init__(self, parent):
        super(DashActions, self).__init__(parent)
        grid = NGridContainer(self)
        grid.setHorizontalSpacing(4)

        self._line = QLineEdit(self)
        self._line.setPlaceholderText('Filter')
        self._line.textChanged.connect(self._lineChanged)

        add   = QPushButton(self)
        add.setIcon(QIcon(sysmapi.nGetPixmap('list-add')))

        clear = QPushButton(self)
        clear.setIcon(QIcon(sysmapi.nGetPixmap('edit-clear')))
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
        print(text)
        #MonitorTreeview.singleton.filterThis(text)
