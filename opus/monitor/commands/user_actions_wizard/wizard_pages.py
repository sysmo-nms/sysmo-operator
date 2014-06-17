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


class Page1(QWizardPage):
    def __init__(self, parent=None, element=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('User actions'))
        self.setSubTitle(self.tr('''
            Configure user actions
        '''))

        grid = NGrid(self)
        grid.addWidget(QLabel(element, self))
        self.setLayout(grid)

        self.setFinalPage(True)

    def nextId(self):
        return -1

    def validatePage(self):
        return False
