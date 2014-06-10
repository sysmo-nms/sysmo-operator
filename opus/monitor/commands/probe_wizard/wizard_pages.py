from PySide.QtGui import (
    QScrollArea,
    QWizardPage,
    QLabel,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QGroupBox,
    QComboBox,
    QSizePolicy,
    QCheckBox,
    QButtonGroup
)

from PySide.QtCore import QSize
from noctopus_widgets import (
    NGrid,
    NGridContainer,
    NFrame,
    NFrameContainer
)
import supercast.main as supercast
import nocapi

class Page1(QWizardPage):
    def __init__(self, parent):
        super(Page1, self).__init__(parent)
        self.completeChanged.connect(self._formComplete)
        self.setFinalPage(False)
        self.setTitle(self.tr('Configure a new check'))
        self.setSubTitle(self.tr('''
            blabla
        '''))
        self._wizard    = parent
        print parent.defs
        self._probeName = parent.probeKey
        self._probeDef  = parent.defs[self._probeName]
        self._defaultIp = parent.defaultIp

        self._mconfig    = dict()
        self._oconfig    = dict()
        self._comline   = ""

        form        = self._generateFormFrame()
        doc         = self._generateDocFrame()
        sim         = self._generateSimFrame()


        layout = NGrid(self)
        layout.addWidget(QLabel(self._probeName, self), 0,0)
        layout.addWidget(form,      1,0)
        layout.addWidget(doc,       1,1)
        layout.addWidget(sim,       2,0,1,2)

        layout.setColumnStretch(0,0)
        layout.setColumnStretch(1,1)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)
        self.setLayout(layout)

    def initializePage(self):
        if self._defaultIp != None:
            self._mconfig['host'].setText(self._defaultIp)
        self._formComplete()

    def _formComplete(self):
        if self.isComplete() == True:
            self._simulateButton.setDisabled(False)
        else:
            self._simulateButton.setDisabled(True)

    def accept(self):
        QDialog.accept(self)
        
    def _generateSimFrame(self):
        simFrame = NFrameContainer(self)
        simLayout   = NGridContainer(simFrame)
        #self._simulateButton = QPushButton(self.tr('Simulate'), self)
        self._simulateButton = QPushButton(self)
        self._simulateButton.setIconSize(QSize(80,80))
        self._simulateButton.setIcon(nocapi.nGetIcon('utilities-terminal'))
        self._simulateButton.clicked.connect(self._simulateComm)
        buttonPol = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._simulateButton.setSizePolicy(buttonPol)
        self._simComm = QTextEdit(self)
        self._simComm.setFixedHeight(100)
        simLayout.addWidget(self._simulateButton, 0,0)
        simLayout.addWidget(self._simComm,  0,1)
        simFrame.setLayout(simLayout)
        self._updateComm('none')
        return simFrame

    def _simulateComm(self):
        self._simulateButton.setDisabled(True)
        self._updateComm(True)
        args = list()
        check = self._probeName
        for key in self._mconfig.keys():
            args.append((key, self._mconfig[key].text()))

        for key in self._oconfig.keys():
            if self._oconfig[key].text() != "":
                args.append((key, self._oconfig[key].text()))
        supercast.send(
            'monitorSimulateCheck',
            (
                check,
                args
            ),
            self.simulateReply
        )

    def simulateReply(self, msg):
        self._simComm.append(msg['value']['info'])
        self._simulateButton.setDisabled(False)

    def _updateComm(self, _):
        comm = '> %s ' % self._probeName
        for key in self._mconfig.keys():
            comm = comm + '--%s=%s ' %(key, self._mconfig[key].text())

        for key in self._oconfig.keys():
            if self._oconfig[key].text() != "":
                comm = comm + '--%s=%s ' %(key, self._oconfig[key].text())
        self._comline = comm
        self._simComm.setText(comm)

    def _generateDocFrame(self):
        self._generateDoc()
        docBox  = QGroupBox(self)
        docBox.setMinimumWidth(600)
        docBox.setTitle(self.tr('Manual'))
        docLayout = NGrid(docBox)
        man = QTextEdit(docBox)
        man.setText(self._man)
        docLayout.addWidget(man)
        docBox.setLayout(docLayout)
        return docBox

    def _generateDoc(self):
        self._man = '<h1>%s</h1>' % self._probeName.title()
        descr = self._probeDef['descr']
        self._man += '<h2>Description</h2><p>%s</p>' % descr

        self._man += '<h3>Mandatory flags</h3>'
        pdefs = self._probeDef['flags_def']
        for pdef in pdefs.keys():
            r = pdefs[pdef]['role']
            if r == 'mandatory':
               name    = pdef
               usage   = pdefs[pdef]['usage']
               self._man += '<h4>--%s=</h4>' % name
               self._man += '<p>%s</p>' % usage

        self._man += '<h3>Options flags</h3>'
        pdefs = self._probeDef['flags_def']
        for pdef in pdefs.keys():
            r = pdefs[pdef]['role']
            if r == 'optional':
               name    = pdef
               usage   = pdefs[pdef]['usage']
               default = pdefs[pdef]['default']
               self._man += '<h4>--%s= (default:%s)</h4>' % (name, default)
               self._man += '<p>%s</p>' % usage

        self._man += '<h3>Informational flags</h3>'
        pdefs = self._probeDef['flags_def']
        for pdef in pdefs.keys():
            r = pdefs[pdef]['role']
            if r == 'informational':
               name    = pdef
               usage   = pdefs[pdef]['usage']
               default = pdefs[pdef]['default']
               self._man += '<h4>--%s</h4>' % name
               self._man += '<p>%s</p>' % usage

    def _generateFormFrame(self):
        pdefs = self._probeDef['flags_def']

        mandatoryBox = QGroupBox(self)
        mandatoryBox.setTitle(self.tr('Mandatory flags'))
        mandatoryFormLayout = QFormLayout(mandatoryBox)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'mandatory':
                self._mconfig[pdef] = QLineEdit(self)
                self._mconfig[pdef].textChanged.connect(self._updateComm)
                self.registerField(
                    '%s*' % pdef,
                    self._mconfig[pdef],
                    changedSignal=pdef)
                mandatoryFormLayout.addRow('-%s' % pdef, self._mconfig[pdef])

        optionalBox = QGroupBox(self)
        optionalBox.setTitle(self.tr('Optional flags'))
        optionalBoxLay = NGrid(optionalBox)
        optionalBox.setLayout(optionalBoxLay)


        optionalScroll  = QScrollArea(optionalBox)
        optionalScroll.setFixedWidth(260)
        optionalScrollFrame = NFrame(optionalScroll)
        optionalFormLayout = QFormLayout(optionalScrollFrame)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'optional':
                self._oconfig[pdef] = QLineEdit(self)
                self._oconfig[pdef].textChanged.connect(self._updateComm)
                optionalFormLayout.addRow('-%s' % pdef, self._oconfig[pdef])
        optionalScrollFrame.setLayout(optionalFormLayout)
        optionalScroll.setWidget(optionalScrollFrame)
        optionalBoxLay.addWidget(optionalScroll, 0,0)

        formFrame = NFrameContainer(self)
        formLayout = NGridContainer(formFrame)
        formLayout.addWidget(mandatoryBox,      0,0)
        formLayout.addWidget(optionalBox,       1,0)
        formFrame.setLayout(formLayout)

        return formFrame

    def nextId(self):
        return 2

    def validatePage(self):
        flags = list()
        for key in self._mconfig.keys():
            flags.append((key, self._mconfig[key].text()))

        for key in self._oconfig.keys():
            if self._oconfig[key].text() != "":
                flags.append((key, self._oconfig[key].text()))

        conf  = dict()
        conf['check']   = self._probeName
        conf['flags']   = flags
        conf['timeout'] = self._mconfig['timeout'].text()
        self._wizard.page1_config = conf
        return True

class Page2(QWizardPage):
    def __init__(self, parent):
        super(Page2, self).__init__(parent)
        pname = parent.probeKey

        self.setFinalPage(False)
        self.setTitle(self.tr('Configure a new check'))
        self.setSubTitle(self.tr('''
            Set step and alerts configuration.
        '''))
        layout = NGrid(self)
        self.setLayout(layout)

        pageFrame = NFrame(self)
        layout.addWidget(pageFrame,    1,1)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,0)
        layout.setColumnStretch(2,1)
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,0)
        layout.setRowStretch(2,1)

        pageForm = QFormLayout(pageFrame)
        pageForm.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        pageForm.setVerticalSpacing(11)
        displayNameLine = QLineEdit(pageFrame)
        displayNameLine.setText('%s: ' % pname)
        self.registerField('p2_display_name*', displayNameLine)
        pageForm.addRow('Display name:', displayNameLine)
        self.step = QSpinBox(self)
        self.registerField('p2_check_step*', self.step)
        pageForm.addRow('Step:',         self.step)
        descrText = QTextEdit(pageFrame)
        self.registerField('p2_description', descrText)
        pageForm.addRow('Description:',  descrText)
        pageFrame.setLayout(pageForm)

    def initializePage(self):
        self.step.setSuffix(" seconds")
        self.step.setMaximum(10000)
        self.step.setValue(300)
        
    def nextId(self):
        return 3

    def validatePage(self):
        return True

class Page3(QWizardPage):
    DO_NOTHING  = 0
    ALERT       = 1
    def __init__(self, parent):
        super(Page3, self).__init__(parent)
        self._wizard = parent
        self.setFinalPage(True)
        self.setTitle(self.tr('Configure a new check'))
        self.setSubTitle(self.tr('''
            Alerts configuration.
        '''))
        layout = NGrid(self)
        self.setLayout(layout)

        alertGroup = QGroupBox(self.tr('Alert behaviour'), self)
        pageGroup = QGroupBox(self.tr('Alert groups'), self)
        layout.addWidget(alertGroup,    1,1)
        layout.addWidget(pageGroup,    1,2)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,0)
        layout.setColumnStretch(2,0)
        layout.setColumnStretch(3,1)
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,0)
        layout.setRowStretch(2,1)

        pageForm = QFormLayout(alertGroup)
        pageForm.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        pageForm.setVerticalSpacing(11)
        onCrit = QComboBox(self)
        onCrit.insertItem(self.DO_NOTHING, 'Do nothing')
        onCrit.insertItem(self.ALERT,      'Send a mail alert')
        pageForm.addRow('On Critical:',  onCrit)
        onWarn = QComboBox(self)
        onWarn.insertItem(self.DO_NOTHING, 'Do nothing')
        onWarn.insertItem(self.ALERT,      'Send a mail alert')
        pageForm.addRow('On Warning:',   onWarn)
        onUnk = QComboBox(self)
        onUnk.insertItem(self.DO_NOTHING, 'Do nothing')
        onUnk.insertItem(self.ALERT,      'Send a mail alert')
        pageForm.addRow('On Unknown:',   onUnk)
        onOk = QComboBox(self)
        onOk.insertItem(self.DO_NOTHING, 'Do nothing')
        onOk.insertItem(self.ALERT,      'Send a mail alert')
        pageForm.addRow('On Ok:',        onOk)
        alertGroup.setLayout(pageForm)

        self._alertsD = dict()
        self._alertsD['CRITICAL']   = onCrit
        self._alertsD['WARNING']    = onWarn
        self._alertsD['UNKNOWN']    = onUnk
        self._alertsD['OK']         = onOk

        groups  = nocapi.nGetGroups()
        glay    = NGrid(pageGroup)
        pageGroup.setLayout(glay)
        self._groupsD = dict()
        for i in range(len(groups)):
            groupName = groups[i]
            self._groupsD[groupName] = QCheckBox(groupName, self)
            glay.addWidget(self._groupsD[groupName], i,0)
            glay.setRowStretch(i, 0)
            glay.setRowStretch(i + 1, 1)

    def nextId(self):
        return -1

    def validatePage(self):
        confDict = dict()
        confDict['alerts'] = list()
        for key in self._alertsD.keys():
            if self._alertsD[key].currentIndex() == Page3.ALERT:
                confDict['alerts'].append(key)

        confDict['groups'] = list()
        for key in self._groupsD.keys():
            if self._groupsD[key].isChecked() == True:
                confDict['groups'].append(key)

        self._wizard.page3_config = confDict
        self._wizard.validateConfig() 
        return True
