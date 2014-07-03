from PySide.QtCore import (
    QObject,
    QSettings,
    Signal
)
from PySide.QtGui import (
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QFormLayout,
    QLabel
)

from noctopus_widgets import (
    NGrid,
    NFrameContainer,
    NGridContainer
)

import nocapi
class DocConfigurator(QDialog):
    def __init__(self, parent=None):
        super(DocConfigurator, self).__init__(parent)
        dialogButtons = QDialogButtonBox(self)
        save = QPushButton('Save', self)
        save.setIcon(nocapi.nGetIcon('document-save'))
        dialogButtons.addButton(save,    QDialogButtonBox.AcceptRole)
        cancel = QPushButton('Cancel', self)
        cancel.setIcon(nocapi.nGetIcon('process-stop'))
        dialogButtons.addButton(cancel,  QDialogButtonBox.RejectRole)

        config      = NFrameContainer(self)
        configGrid  = NGrid(self)
        config.setLayout(configGrid)

        grid = NGrid(self)
        grid.addWidget(QLabel('config', self),  0,0)
        grid.addWidget(dialogButtons,           1,0)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,0)
        self.setLayout(grid)

        self.exec_()
