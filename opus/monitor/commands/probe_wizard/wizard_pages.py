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
    QComboBox
)

from noctopus_widgets import (
    NGrid,
    NGridContainer,
    NFrame,
    NFrameContainer
)
import supercast.main as supercast

class Page1(QWizardPage):
    def __init__(self, probeDefs, probeKey, defaultIp, parent):
        super(Page1, self).__init__(parent)
        self._defaultIp = defaultIp
        self.setFinalPage(False)
        self.setTitle(self.tr('Configure a new check'))
        self.setSubTitle(self.tr('''
            blabla
        '''))
        self._caller    = parent
        self._probeDef  = probeDefs[probeKey]
        self._probeName = probeKey
        self._config    = dict()
        self._comline   = ""

        form        = self._generateFormFrame()
        doc         = self._generateDocFrame()
        sim         = self._generateSimFrame()

        if self._defaultIp != None:
            self._config['host'].setText(defaultIp)

        layout = NGrid(self)
        layout.addWidget(QLabel(probeKey, self), 0,0)
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

    def accept(self):
        print "aaaaaaaaaaaaaccept"
        QDialog.accept(self)
        
    def _generateSimFrame(self):
        simFrame = NFrameContainer(self)
        simLayout   = NGridContainer(simFrame)
        simulateButton = QPushButton(self.tr('Simulate'), self)
        simulateButton.clicked.connect(self._simulateComm)
        self._simComm = QTextEdit(self)
        self._simComm.setFixedHeight(100)
        simLayout.addWidget(simulateButton, 0,0)
        simLayout.addWidget(self._simComm,  1,0)
        simFrame.setLayout(simLayout)
        self._updateComm('none')
        return simFrame

    def _simulateComm(self):
        args = list()
        path = self._probeDef['path']
        for key in self._config.keys():
            args.append((key, self._config[key].text()))
        print args
        supercast.send(
            'monitorSimulateCheck',
            (
                path,
                args
            ),
            self.simulateReply
        )

    def simulateReply(self, msg):
        print "reply !!!!!!!!! msg"

    def _updateComm(self, _):
        comm = '> %s ' % self._probeName
        for key in self._config.keys():
            comm = comm + '--%s=%s ' %(key, self._config[key].text())
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
                self._config[pdef] = QLineEdit(self)
                self._config[pdef].textChanged.connect(self._updateComm)
                mandatoryFormLayout.addRow('-%s' % pdef, self._config[pdef])

        optionalBox = QGroupBox(self)
        optionalBox.setTitle(self.tr('Optional flags'))
        optionalBoxLay = NGrid(optionalBox)
        optionalBox.setLayout(optionalBoxLay)

        optionalScroll  = QScrollArea(optionalBox)
        #optionalScroll.setFixedHeight(160)
        optionalScroll.setFixedWidth(260)
        optionalScrollFrame = NFrame(optionalScroll)
        optionalFormLayout = QFormLayout(optionalScrollFrame)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'optional':
                optionalFormLayout.addRow('-%s' % pdef, QLineEdit(self))
        optionalScrollFrame.setLayout(optionalFormLayout)
        optionalScroll.setWidget(optionalScrollFrame)
        optionalBoxLay.addWidget(optionalScroll, 0,0)



        #informationalBox = QGroupBox(self)
        #informationalBox.setTitle(self.tr('Informational flags'))
        #informationalFormLayout = QFormLayout(informationalBox)
        #for pdef in pdefs.keys():
            #if pdefs[pdef]['role'] == 'informational':
                #informationalFormLayout.addRow('-%s' % pdef, QLineEdit(self))

        formFrame = NFrameContainer(self)
        formLayout = NGridContainer(formFrame)
        formLayout.addWidget(mandatoryBox,      0,0)
        formLayout.addWidget(optionalBox,       1,0)
        #formLayout.addWidget(informationalBox,  2,0)
        formFrame.setLayout(formLayout)

        return formFrame

    def nextId(self):
        return 2

    def validatePage(self):
        print "validate probe wiz"
        return True

class Page2(QWizardPage):
    def __init__(self, parent):
        super(Page2, self).__init__(parent)
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
        pageForm.addRow('Display name:', QLineEdit(pageFrame))
        step = QSpinBox(self)
        step.setSuffix(" seconds")
        step.setMaximum(10000)
        step.setValue(300)
        pageForm.addRow('Step:',         step)
        #pageForm.addRow('On Critical:',  QComboBox(self))
        #pageForm.addRow('On Warning:',   QComboBox(self))
        #pageForm.addRow('On Unknown:',   QComboBox(self))
        #pageForm.addRow('On Ok:',        QComboBox(self))
        pageForm.addRow('Description:',  QTextEdit(pageFrame))
        pageFrame.setLayout(pageForm)

    def nextId(self):
        return 3

    def validatePage(self):
        print "vvv"
        return True

class Page3(QWizardPage):
    def __init__(self, parent):
        super(Page3, self).__init__(parent)
        self.setFinalPage(True)
        self.setTitle(self.tr('Configure a new check'))
        self.setSubTitle(self.tr('''
            Alerts configuration.
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
        pageForm.addRow('On Critical:',  QComboBox(self))
        pageForm.addRow('On Warning:',   QComboBox(self))
        pageForm.addRow('On Unknown:',   QComboBox(self))
        pageForm.addRow('On Ok:',        QComboBox(self))
        pageFrame.setLayout(pageForm)

    def nextId(self):
        return -1

    def validatePage(self):
        print "vvv"
        return False
