from PyQt5.QtGui   import (
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
    QListWidget,
    QMessageBox,
    QMenu,
    QAction
)
from PyQt5.QtCore import Qt

from noctopus_widgets import (
    NGrid,
    NFrame,
    NGridContainer,
    NFrameContainer,
    NMenuButton
)
from functools import partial
import nocapi
import opus.monitor.api as monapi


class Page1(QWizardPage):
    def __init__(self, parent=None, element=None):
        super(Page1, self).__init__(parent)
        self.setTitle(self.tr('User actions'))
        self.setSubTitle(self.tr('''
            Configure user actions
        '''))
        self.setFinalPage(True)
        self._elementName = element
        self._elementType = None


        #self._propertyBox = QGroupBox(self.tr('Property binds'), self)
        #self._fillPropertiesBox()

        #self._actionsBox  = QGroupBox(self.tr('Actions'), self)
        #self._fillActionBox()
        # layout

        self._commButton = NMenuButton(self)
        self._commButton.setIcon(nocapi.nGetIcon('list-add'))
        self._commButton.setText(self.tr('Add action'))
        self._commMenu  = QMenu(self)
        self._commButton.setMenu(self._commMenu)
        self._fillCommButton()

        self._actionList = QListWidget(self)
        self._fillActionList()

        grid = NGrid(self)
        grid.setContentsMargins(5,10,5,5)
        grid.setVerticalSpacing(20)
        grid.addWidget(self._commButton,   0,0,1,1)
        grid.addWidget(self._actionList,   0,1,2,1)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        self.setLayout(grid)
        # layout end

    def _fillActionList(self):
        actions = monapi.getUActionsFor(self._elementName)
        for i in range(len(actions)):
            self._actionList.addItem(actions[i])


    def _fillCommButton(self):
        self._uactions = monapi.getUActionsCmds()
        self._commList  = list()
        index           = 0
        for key in list(self._uactions.keys()):
            qact = QAction(key,self)
            qact.triggered.connect(partial(self._addAction, key))
            self._commMenu.addAction(qact)

    def _addAction(self, action):
        monapi.addTargetAction(action, self._elementName)
        self._actionList.addItem(action)

    def nextId(self):
        return -1

    def validatePage(self):
        return True
