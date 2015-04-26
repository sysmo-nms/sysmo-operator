from PyQt5.QtWidgets import QWizard, QWizardPage, QAbstractItemView, QTreeView, QHeaderView, QLineEdit, QPushButton, QLabel, QFormLayout, QTextEdit, QFrame, QGridLayout, QAbstractScrollArea, QWidget, QSpinBox, QLineEdit, QCheckBox, QDialog, QTreeWidget, QTreeWidgetItem, QDialogButtonBox, QErrorMessage
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QPalette
from PyQt5.QtCore import Qt, QSortFilterProxyModel, pyqtSignal
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
        treeView.doubleClicked.connect(self._doubleClick)
        clearButton.clicked.connect(treeView.clearSelection)
        clearButton.clicked.connect(self.completeChanged)

        model = QStandardItemModel(self)
        model.setColumnCount(2)
        model.setHorizontalHeaderLabels(['Class', 'Type', 'Description'])
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
            xml_Description = xml_checks[ckey].find('nchecks:Description', nchecks.NS)
            ptype = xml_checks[ckey].attrib['Type']
            pitem = QStandardItem()
            pitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            pitem.setData(ckey, Qt.DisplayRole)
            pitem.setData(ckey, Qt.UserRole)
            ditem = QStandardItem()
            ditem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            ditem.setData(xml_Description.text, Qt.DisplayRole)
            ditem.setData(ckey, Qt.UserRole)
            titem = QStandardItem()
            titem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            titem.setData(ptype, Qt.DisplayRole)
            titem.setData(ckey, Qt.UserRole)
            model.appendRow([pitem, titem, ditem])

        treeView.header().setSortIndicatorShown(True)
        treeView.setSortingEnabled(True)
        treeView.header().resizeSections(QHeaderView.ResizeToContents)

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

    def _doubleClick(self, val):
        self._wizard.setSelection(val.data(Qt.UserRole))
        self._wizard.next()

    def isComplete(self):
        sel = self._treeView.selectedIndexes()
        if len(sel) == 0:
            return False
        else:
            u = sel[0]
            self._wizard.setSelection(u.data(Qt.UserRole))
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
        self._xml_Check = xml_Check
        self._ptype = xml_Check.attrib['Type']

        # initialize textEdit content and old layout
        doc = ""
        # cleanup
        self.cleanupPage()

        # create h1
        doc += "<h1>%s</h1>" % probe
        # create p descr
        xml_Description = xml_Check.find('nchecks:Description', nchecks.NS)
        doc += "<p>%s</p>" % xml_Description.text
        
        xml_FlagTable   = xml_Check.find('nchecks:FlagTable', nchecks.NS)
        xml_HelperTable = xml_Check.find('nchecks:HelperTable', nchecks.NS)

        # interage FlagTable
        for xml_Flag in xml_FlagTable.findall('nchecks:Flag', nchecks.NS):
            #if 'AutoFill' in xml_Flag.attrib:
            # generate doc
            xml_Default = xml_Flag.find('nchecks:Default', nchecks.NS)
            xml_Usage = xml_Flag.find('nchecks:Usage', nchecks.NS)
            xml_Hint = xml_Flag.find('nchecks:Hint', nchecks.NS)

            doc += "<h4>--%s=%s  (default:%s)</h4><p>%s</p>" % (
                xml_Flag.attrib['Id'],
                xml_Flag.attrib['Type'],
                xml_Default.text,
                xml_Usage.text)

            if   xml_Flag.attrib['Type'] == 'integer':
                w = NSpinBox(self)
                w.setMinimum(ast.literal_eval(xml_Flag.attrib['Minimum']))
                w.setMaximum(ast.literal_eval(xml_Flag.attrib['Maximum']))
                w.setValue(ast.literal_eval(xml_Default.text))
                if 'AutoFill' in xml_Flag.attrib:
                    prop = xml_Flag.attrib['AutoFill']
                    val = self.getProperty(prop)
                    if val != False: w.setValue(ast.literal_eval(val))
            elif xml_Flag.attrib['Type'] == 'string':
                w = NLineEdit(self)
                w.setText(xml_Default.text)
                if 'AutoFill' in xml_Flag.attrib:
                    prop = xml_Flag.attrib['AutoFill']
                    val = self.getProperty(prop)
                    if val != False: w.setText(val)

            elif xml_Flag.attrib['Type'] == 'boolean':
                w = NCheckBox(self)
                if xml_Default.text == "true":
                    w.setChecked(True)
                else:
                    w.setChecked(False)

            w.setToolTip(xml_Hint.text)
            if 'HelperButton' in xml_Flag.attrib:
                xml_HelperList = xml_HelperTable.findall('nchecks:Helper', nchecks.NS)
                xml_Helper = None
                for xml_Helper in xml_HelperList:
                    if xml_Helper.attrib['Id'] == xml_Flag.attrib['HelperButton']:
                        break
                        
                f = QFrame(self)
                g = QGridLayout(f)
                b = HelperButton(xml_Helper.attrib['Class'], f)
                b.triggered[str].connect(self._launchHelper)
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

        # check for helpers
        self._HelperTable = xml_HelperTable
        start_list = list()

        # is there any helper we need to start now?
        if xml_HelperTable == None: return

        for xml_Helper in xml_HelperTable.findall('nchecks:Helper', nchecks.NS):
            if xml_Helper.attrib['AutoStart'] == "true":
                start_list.append(xml_Helper)

        
        # then start them now
        for xml_Helper in start_list:
            helperClass = xml_Helper.attrib['Class']
            self._launchHelper(helperClass)
            

    def _launchHelper(self, helper):
        pdu = {
            'from': 'monitor',
            'type': 'ncheckHelperQuery',
            'value': {
                'target': self._target,
                'class':  helper,
                'type':   self._ptype
            }
        }
        supercast.send(pdu, self._helperReply)

    def _helperReply(self, msg):
        if msg['value']['reply']['status'] == "failure":
            print("say failure for helper %s [Close]" % msg['value']['reply']['id'])
            err = QErrorMessage(self)
            print("error? " + str(msg))
            mid = msg['value']['reply']['id']
            mreason = msg['value']['reply']['message']
            errmsg = "The helper %s has failed with reason: %s" % (mid,mreason)
            err.showMessage(errmsg)
            err.exec()

        else:
            dial = HelperDialog(msg['value']['reply'], self._HelperTable, self)
            dial.exec()
        sys.stdout.flush()

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

    def setFlagVal(self, flag, value):
        self._widgetDict[flag].setText(value)

class HelperDialog(QDialog):
    def __init__(self, msg, helperTable, parent=None):
        QDialog.__init__(self, parent)
        helperId = msg['id']
        self._helperMsg = msg
        self._xml_Helper = None
        for helper in helperTable.findall('nchecks:Helper', nchecks.NS):
            if helper.attrib['Id'] == helperId:
                self._xml_Helper = helper
                

        self.setModal(True)
        self.setSizeGripEnabled(True)
        self.setWindowTitle("%s Helper" % msg['id'])
        if self._xml_Helper.attrib['Return'] == "table":
            self._initTableLayout()

    def _initTableLayout(self):
        grid = QGridLayout(self)
        xml_HelperTableReturn = self._xml_Helper.find(
                                        'nchecks:HelperTableReturn', nchecks.NS)
        # init usage label
        xml_Usage = xml_HelperTableReturn.find('nchecks:Usage', nchecks.NS)
        usage = QLabel(xml_Usage.text, self)

        # init treeview
        tview = QTreeWidget(self)

        # init headers
        xml_Column_list = xml_HelperTableReturn.findall('nchecks:Column', nchecks.NS)
        colLen = len(xml_Column_list)
        tviewHeaders = [None] * colLen
        for xml_Column in xml_Column_list:
            cid = xml_Column.attrib['Id']
            cpos = int(xml_Column.attrib['Position'])
            tviewHeaders[cpos] = cid
            ctype = xml_Column.attrib['Type']
        tview.setHeaderLabels(tviewHeaders)
        tview.header().setSortIndicatorShown(True)
        tview.setSortingEnabled(True)

        # if TreeRoot is defined create root items and fill the rest
        treeRoot = xml_HelperTableReturn.attrib['TreeRoot']
        selectType = xml_HelperTableReturn.attrib['SelectionType']
        print("kkkkkkkkkkkkkkkkkkk" + str(treeRoot))

        # what is the element we want to get
        # what is the flag we want to fill
        self._fillFlag = xml_HelperTableReturn.attrib['FillFlag']
        xml_ListSeparator = xml_HelperTableReturn.find(
                                        'nchecks:ListSeparator', nchecks.NS)
        self._fillFlagSeparator = xml_ListSeparator.text

        if treeRoot != None and selectType == "multiple":
        # here we want a tree view with root and childs elements (depy 1), that
        # are checkables.
            tview.setSelectionMode(QAbstractItemView.NoSelection)

            # get all treeRoot types
            self._rootItems = dict()
            trtypes = list()
            for t in self._helperMsg['rows']:
                tval = t[treeRoot]
                if tval not in trtypes:
                    trtypes.append(tval)
            # then create initial root items
            for t in trtypes:
                txt = "%s(%s)" % (treeRoot, t)
                item = QTreeWidgetItem(tview, [txt], QTreeWidgetItem.Type)
                item.setCheckState(0, Qt.Unchecked)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                tview.addTopLevelItem(item)
                self._rootItems[t] = item

            # then add child items
            for ch in self._helperMsg['rows']:
                selectKey = xml_HelperTableReturn.attrib['Select']
                roottype = ch[treeRoot]
                chtext = list()
                # use the tviewHeaders wich contain an ordered list of property
                itemData = None
                for col in tviewHeaders:
                    if col == selectKey:
                        itemData = ch[col]
                    chtext.append(ch[col])
                item = CustomItem(chtext, QTreeWidgetItem.Type, itemData)
                item.setCheckState(0, Qt.Unchecked)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                self._rootItems[roottype].addChild(item)
            tview.itemChanged[QTreeWidgetItem, int].connect(
                    self._refreshRootTableCheckStates)

        elif treeRoot != None and selectType == "single":
        # TODO here we want a tree view with root and childs elements (deph 1)
        # only one can be highlighted
            treeView.setSelectionMode(QAbstractItemView.SingleSelection)
        elif selectType == "multiple":
        # TODO here we want a table view that where multiple elements can be checked
            treeView.setSelectionMode(QAbstractItemView.NoSelection)
        elif selectType == "single":
            treeView.setSelectionMode(QAbstractItemView.SingleSelection)
        # TODO here we want a table view with a single element to selected

        tview.header().resizeSections(QHeaderView.ResizeToContents)
        tview.expandAll()

        buttons = QDialogButtonBox(self)
        buttons.addButton(QDialogButtonBox.Save)
        buttons.addButton(QDialogButtonBox.Cancel)
        self._saveButton = buttons.button(QDialogButtonBox.Save)
        self._saveButton.setEnabled(False)
        buttons.rejected.connect(self.deleteLater)
        buttons.accepted.connect(self._accepted)

        # final grid
        grid.addWidget(usage, 0,0)
        grid.addWidget(tview, 1,0)
        grid.addWidget(buttons, 2,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,0)
        

    def _accepted(self):
        rep = list()
        for key in self._rootItems.keys():
            root = self._rootItems[key]
            cc = root.childCount()
            for i in range(cc):
                if root.child(i).checkState(0) == Qt.Checked:
                    rep.append(root.child(i).getData())

        rep = sorted(rep)
        repstr = ""
        first = True
        for v in rep:
            if first == True:
                repstr = repstr + v
                first = False
            else: repstr = repstr + self._fillFlagSeparator + v

        self.parent().setFlagVal(self._fillFlag, repstr)
        self.close()

    def _refreshRootTableCheckStates(self, item, column):
        childCount = item.childCount()
        if childCount > 0:
        # it is a root item
            if item.checkState(0) == Qt.PartiallyChecked: return
            rootstate = item.checkState(0)
            for i in range(childCount):
                ch = item.child(i)
                if ch.checkState(0) != rootstate:
                    ch.setCheckState(0,rootstate)
        
        # it is a child item
        else:
            # get the root item
            root = item.parent()
            # get the number of childs
            rcount = root.childCount()
            cstates = list()
            for i in range(rcount):
                citem = root.child(i)
                cstates.append(citem.checkState(0))

            # we now have childs state in cstates
            if Qt.Unchecked in cstates and Qt.Checked in cstates:
                # if states are mixed root is tristate
                if root.checkState(0) != Qt.PartiallyChecked:
                    root.setCheckState(0,Qt.PartiallyChecked)
            elif Qt.Checked in cstates:
            # if all state is checked root is checked
                if root.checkState(0) != Qt.Checked:
                    root.setCheckState(0,Qt.Checked)
            elif Qt.Unchecked in cstates:
            # if all state is unchecked root is unchecked
                if root.checkState(0) != Qt.Unchecked:
                    root.setCheckState(0,Qt.Unchecked)
        self._maybeEnableSave()

    def _maybeEnableSave(self):
        for key in self._rootItems.keys():
            root = self._rootItems[key]
            cc = root.childCount()
            for i in range(cc):
                if root.child(i).checkState(0) == Qt.Checked:
                    self._saveButton.setEnabled(True)
                    return
        self._saveButton.setEnabled(False)


class CustomItem(QTreeWidgetItem):
    def __init__(self, text, itemType, itemData):
        QTreeWidgetItem.__init__(self, text, itemType)
        self._data = itemData

    def getData(self): return self._data

class HelperButton(QPushButton):
    triggered = pyqtSignal(str)
    def __init__(self, helperClass, parent=None):
        QPushButton.__init__(self, parent)
        self.setText('Helper')
        self._helperClass = helperClass
        self.clicked.connect(self._trigger)

    def _trigger(self):
        self.triggered.emit(self._helperClass)

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
