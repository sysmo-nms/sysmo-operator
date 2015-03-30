from PyQt5.QtWidgets import QWizard, QWizardPage, QAbstractItemView, QTreeView, QHeaderView, QLineEdit, QPushButton, QLabel, QFormLayout, QTextEdit, QFrame, QAbstractScrollArea, QWidget, QSpinBox, QLineEdit, QCheckBox
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QPalette
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from sysmo_widgets import NFrame, NGrid, NGridContainer
import sysmo_main
import sysmapi
import nchecks
import ast
import monitor.api as monapi
import supercast.main as supercast

import sys

class NewProbe(QWizard):
    def __init__(self, target, parent=None):
        # give parent the QMainWindow to open at the center of it
        parent = sysmo_main.NMainWindow.singleton
        super(NewProbe, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setModal(True)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
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
        self.setCommitPage(True)
        

        self._lab = QLabel(self)
        self._config     = QFormLayout(self)
        self._manual     = QTextEdit(self)

        manFrame = NFrame(self)
        manFrame.setFrameShape(QFrame.Box)
        manLayout = NGridContainer(manFrame)
        manLayout.addWidget(self._manual)


        confFrame = QAbstractScrollArea(self)
        confFrame.setMinimumWidth(300)
        confFrame.setFrameShape(QFrame.Box)
        confFrame.setLayout(self._config)
        
        
        grid = NGrid(self)
        grid.addWidget(self._lab,   0,0,1,2)
        grid.addWidget(confFrame,   1,0)
        grid.addWidget(manFrame,    1,1)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)

        self._widgetDict = dict()
        self._configFrame = confFrame
        self._wizard = parent
        self._target = target
        self._end = False


    def initializePage(self):
        probe = self._wizard.getSelection()
        self._probe = probe
        self.setSubTitle('%s configuration form' % probe)
        self._lab.setText(probe)

        # get the probe def
        pdef = self._wizard.probesDict[probe]

        # initialize textEdit content and old layout
        text = ""
        # cleanup
        self.cleanupPage()

        # create h1
        text += "<h1>%s</h1>" % probe
        # create p descr
        text += "<p>%s</p>" % pdef['descr']
        
        # iterate flag_infos
        finfo = pdef['flag_info']
        for fdef in finfo:
            flag    = fdef['name']
            usage   = fdef['usage']
            hint    = fdef['hint']
            role    = fdef['role']
            default = fdef['default']
            ftype   = fdef['type']

            # generate doc
            text += "<h4>--%s=%s  (default:%s)</h4>" % (flag, ftype, default)
            text += "<p>%s</p>" % usage

            # build form
            if ftype == 'int':
                widget = NSpinBox(self)
                widget.setMinimum(0)
                widget.setMaximum(65535)
                if default != None:
                    widget.setValue(ast.literal_eval(default))
            elif ftype == 'bool':
                widget = NCheckBox(self)
                if default == "false":
                    widget.setChecked(False)
                if default == "true":
                    widget.setChecked(True)
                else:
                    widget.setChecked(False)
            else:
                widget = NLineEdit(self)
                if default != None:
                    widget.setText(default)
            
            widget.setToolTip(hint)
            self._widgetDict[flag] = widget
            
            self._config.addRow(flag, widget)
            
        # set host flag to target host property
        t = monapi.getTarget(self._target)
        host = t['properties']['host']
        self._widgetDict['host'].setText(host)
        self._manual.setText(text)

    def cleanupPage(self):
        self._lab.setText('')
        QWidget().setLayout(self._config)
        self._config = QFormLayout(self._configFrame)
        del self._widgetDict
        self._widgetDict = dict()

    
    def nextId(self): return -1
    
    def validatePage(self):
        # send command via supercast
        if self._end == True: return True
        propDict = dict()
        for flag in self._widgetDict.keys():
            propDict[flag] = self._widgetDict[flag].nGet()

        pdu = {
            'from': 'monitor',
            'type': 'createNchecksQuery',
            'value': {
                'target': self._target,
                'name':   self._probe,
                'properties': propDict
            }
        }
        print(str(pdu))
        supercast.send(pdu, self._createNcheckReply)
        return False

    def _createNcheckReply(self, msg):
        self._end = True
        self._wizard.accept()
        print("have returned?")

class NLineEdit(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        
    def nGet(self):
        return self.text()

class NCheckBox(QCheckBox):
    def __init__(self, parent):
        QCheckBox.__init__(self, parent)
        
    def nGet(self):
        if self.checkState() == True:
            return "true"
        else:
            return "false"

class NSpinBox(QSpinBox):
    def __init__(self, parent):
        QSpinBox.__init__(self, parent)

    def nGet(self):
        return self.value()
