from PySide.QtCore import (
    QObject,
    QSettings,
    Signal
)
from PySide.QtGui import (
    QDialog,
    QDialogButtonBox,
    QLabel
)

from noctopus_widgets import (
    NGrid,
    NGridContainer
)

class DocConfigurator(QDialog):
    def __init__(self, parent=None):
        super(DocConfigurator, self).__init__(parent)
        grid = NGrid(self)
        dialogButtons = QDialogButtonBox(self)
        grid.addWidget(dialogButtons,   1,0)
        self.setLayout(grid)
