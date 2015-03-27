from PyQt5.QtWidgets import QWizard, QWizardPage, QAbstractItemView, QTreeView, QHeaderView, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from sysmo_widgets import NFrame, NGrid
import sysmo_main
import sysmapi
import nchecks

import sys

class NewProbe(QWizard):
    def __init__(self, target, parent=None):
        # give parent the QMainWindow to open at the center of it
        parent = sysmo_main.NMainWindow.singleton
        super(NewProbe, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setModal(True)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)

        self.probesDict = nchecks.getProbesDef()
        self.setPage(1, ProbeSelectionPage(target, self))
        self.setPage(2, ProbeConfigurationPage(target, self))
        self.setStartId(1)
    
    def setSelection(self, probe):
        self._selection = probe
    
    def getSelection(self):
        return self._selection

class ProbeSelectionPage(QWizardPage):
    def __init__(self, target, parent):
        super(ProbeSelectionPage, self).__init__(parent)
        self.setTitle('New probe for target %s' % target)
        self.setSubTitle('Select a probe from the following list')
        self.setFinalPage(False)
        pr = parent.probesDict
        grid = NGrid(self)
        searchLine  = QLineEdit(self)
        searchLine.setPlaceholderText('Filter')
        clearButton = QPushButton(self)
        clearButton.setFixedWidth(30)
        clearButton.setContentsMargins(0,0,0,0)
        clearButton.clicked.connect(searchLine.clear)
        clearButton.setIcon(QIcon(sysmapi.nGetPixmap('edit-clear')))

        treeView = QTreeView(self)
        treeView.setSelectionMode(QAbstractItemView.SingleSelection)
        treeView.clicked.connect(self.completeChanged)
        treeView.doubleClicked.connect(self._test)
        clearButton.clicked.connect(treeView.clearSelection)
        clearButton.clicked.connect(self.completeChanged)

        model = QStandardItemModel(self)
        model.setColumnCount(2)
        model.setHorizontalHeaderLabels(['Probe name', 'Description'])
        proxyFilter = QSortFilterProxyModel(self)
        proxyFilter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxyFilter.setDynamicSortFilter(True)
        proxyFilter.setFilterRole(Qt.DisplayRole)
        proxyFilter.setSourceModel(model)
        proxyFilter.setFilterKeyColumn(-1)
        treeView.setModel(proxyFilter)
        searchLine.textChanged[str].connect(proxyFilter.setFilterFixedString)
        searchLine.textChanged.connect(self.completeChanged)

        for pkey in pr.keys():
            pitem = QStandardItem()
            pitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            pitem.setData(pkey, Qt.DisplayRole)
            ditem = QStandardItem()
            ditem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            ditem.setData(pr[pkey]['descr'], Qt.DisplayRole)
            model.appendRow([pitem, ditem])

        grid.addWidget(clearButton, 0,0)
        grid.addWidget(searchLine,  0,1)
        grid.addWidget(treeView, 1,0,1,3)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)

        self._treeView = treeView
        self._model = model
        self._searchLine = searchLine
        self._wizard = parent

    def initializePage(self):
        self._treeView.clearSelection()
        self._searchLine.clear()

    def cleanupPage(self):
        self._treeView.clearSelection()
        self._searchLine.clear()

    def nextId(self): return 2

    def _test(self, val):
        row = val.row()
        col = val.column()
        if col == 0:
            probe = val.data(Qt.DisplayRole)
        else:
            val2 = self._model.index(row, 0)
            probe = val2.data(Qt.DisplayRole)
        
        self._wizard.setSelection(probe)
        self._wizard.next()

    def isComplete(self):
        sel = self._treeView.selectedIndexes()
        if len(sel) == 0:
            return False
        else:
            self._wizard.setSelection(sel[0].data(Qt.DisplayRole))
            return True
        

class ProbeConfigurationPage(QWizardPage):
    def __init__(self, target, parent):
        super(ProbeConfigurationPage, self).__init__(parent)
        self.setTitle('New probe for target %s' % target)
        self.setSubTitle('Probe configuration')
        self.setFinalPage(True)
        self._lab = QLabel(self)
        self._wizard = parent

    def initializePage(self):
        self._lab.setText(self._wizard.getSelection())
        
    def cleanupPage(self):
        self._lab.setText('')
