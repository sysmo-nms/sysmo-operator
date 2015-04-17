from PyQt5.QtWidgets import QWizard, QWizardPage, QAbstractItemView, QTreeView, QHeaderView, QLineEdit, QPushButton, QLabel, QFormLayout, QTextEdit, QFrame, QGridLayout, QAbstractScrollArea, QWidget, QSpinBox, QLineEdit, QCheckBox
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
        self._xmlChecks = nchecks.getChecks()
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
        xml_checks = parent._xmlChecks
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

        for ckey in xml_checks.keys():
            pitem = QStandardItem()
            pitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            pitem.setData(ckey, Qt.DisplayRole)
            ditem = QStandardItem()
            ditem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            ditem.setData(xml_checks[ckey].attrib['Descr'], Qt.DisplayRole)
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
        xml_Check = self._wizard._xmlChecks[probe]

        # initialize textEdit content and old layout
        doc = ""
        # cleanup
        self.cleanupPage()

        # create h1
        doc += "<h1>%s</h1>" % probe
        # create p descr
        doc += "<p>%s</p>" % xml_Check.attrib['Descr']
        
        xml_FlagTable   = xml_Check.find('nchecks:FlagTable', nchecks.NS)
        xml_HelperTable = xml_Check.find('nchecks:HelperTable', nchecks.NS)

        # interage FlagTable
        for xml_Flag in xml_FlagTable.findall('nchecks:Flag', nchecks.NS):
            #if 'AutoFill' in xml_Flag.attrib:
            # generate doc
            doc += "<h4>--%s=%s  (default:%s)</h4><p>%s</p>" % (
                xml_Flag.attrib['Id'],
                xml_Flag.attrib['Type'],
                xml_Flag.attrib['Default'],
                xml_Flag.attrib['Usage'])

            if   xml_Flag.attrib['Type'] == 'integer':
                w = NSpinBox(self)
                w.setMinimum(ast.literal_eval(xml_Flag.attrib['Min']))
                w.setMaximum(ast.literal_eval(xml_Flag.attrib['Max']))
                w.setValue(ast.literal_eval(xml_Flag.attrib['Default']))
                if 'AutoFill' in xml_Flag.attrib:
                    prop = xml_Flag.attrib['AutoFill']
                    val = self.getProperty(prop)
                    if val != False: w.setValue(ast.literal_eval(val))
            elif xml_Flag.attrib['Type'] == 'string':
                w = NLineEdit(self)
                w.setText(xml_Flag.attrib['Default'])
                if 'AutoFill' in xml_Flag.attrib:
                    prop = xml_Flag.attrib['AutoFill']
                    val = self.getProperty(prop)
                    if val != False: w.setText(val)

            elif xml_Flag.attrib['Type'] == 'boolean':
                w = NCheckBox(self)
                if xml_Flag.attrib['Default'] == "true":
                    w.setChecked(True)
                else:
                    w.setChecked(False)

            w.setToolTip(xml_Flag.attrib['Hint'])
            if 'Helper' in xml_Flag.attrib:
                f = QFrame(self)
                g = QGridLayout(f)
                b = QPushButton('Helper', f)
                g.addWidget(QLabel(xml_Flag.attrib['Id'], self), 0,0)
                g.addWidget(w, 0,1)
                g.addWidget(b, 0,2)
                g.setColumnStretch(0,0)
                g.setColumnStretch(1,1)
                g.setColumnStretch(2,0)
                self._widgetDict[xml_Flag.attrib['Id']] = w
                self._config.addRow(f)
            else:
                self._widgetDict[xml_Flag.attrib['Id']] = w
                self._config.addRow(xml_Flag.attrib['Id'], w)

        self._manual.setText(doc)

    def getProperty(self, prop):
        t = monapi.getTarget(self._target)
        if prop in t['properties']:
            return t['properties'][prop]
        else:
            return False
        
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
