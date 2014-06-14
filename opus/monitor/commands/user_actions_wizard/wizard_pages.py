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
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('User actions'))
        self.setSubTitle(self.tr('''
            Configure user actions
        '''))
        self.setFinalPage(True)

    def nextId(self):
        return -1

    def validatePage(self):
        return False
