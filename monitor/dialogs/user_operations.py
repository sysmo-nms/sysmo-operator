from PyQt5.QtWidgets import QWizard, QWizardPage, QMenu, QListWidget, QAction
from functools import partial
from sysmo_widgets import NGrid, NMenuButton
import sysmapi
import monitor.api as monapi


class UserOperationsWizard(QWizard):
    def __init__(self, parent=None, element=None):
        super(UserOperationsWizard, self).__init__(parent)

        self.setModal(True)
        page1 = Page1(self, element)
        self.setPage(1, page1)
        self.setStartId(1)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPixmap(QWizard.WatermarkPixmap, sysmapi.nGetPixmap('console'))
        self.setPixmap(QWizard.LogoPixmap,sysmapi.nGetPixmap('applications-system'))
        self.show()

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

        #self._actionsBox  = QGroupBox(self.tr('Operations'), self)
        #self._fillOperationBox()
        # layout

        self._commButton = NMenuButton(self)
        self._commButton.setIcon(sysmapi.nGetIcon('list-add'))
        self._commButton.setText(self.tr('Add action'))
        self._commMenu  = QMenu(self)
        self._commButton.setMenu(self._commMenu)
        self._fillCommButton()

        self._actionList = QListWidget(self)
        self._fillOperationList()

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

    def _fillOperationList(self):
        actions = monapi.getUOperationsFor(self._elementName)
        for i in range(len(actions)):
            self._actionList.addItem(actions[i])


    def _fillCommButton(self):
        self._uactions = monapi.getUOperationsCmds()
        self._commList  = list()
        index           = 0
        for key in list(self._uactions.keys()):
            qact = QAction(key,self)
            qact.triggered.connect(partial(self._addOperation, key))
            self._commMenu.addAction(qact)

    def _addOperation(self, action):
        monapi.addTargetOperation(action, self._elementName)
        self._actionList.addItem(action)

    def nextId(self):
        return -1

    def validatePage(self):
        return True
