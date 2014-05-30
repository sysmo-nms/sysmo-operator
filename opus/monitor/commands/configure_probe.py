from PySide.QtGui import (
    QDialog,
    QLabel,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDialogButtonBox,
    QPushButton,
    QGroupBox
)

from noctopus_widgets import (
    NGrid,
    NGridContainer,
    NFrameContainer
)
import supercast.main as supercast

class ProbeForm(QDialog):
    def __init__(self, probeDefs, probeKey, parent):
        super(ProbeForm, self).__init__(parent)
        self.setModal(True)
        self._caller    = parent
        self._probeDef  = probeDefs[probeKey]
        self._probeName = probeKey
        self._config    = dict()
        self._comline   = ""

        form        = self._generateFormFrame()
        doc         = self._generateDocFrame()
        sim         = self._generateSimFrame()

        buttons     = QDialogButtonBox.Save|QDialogButtonBox.Cancel|QDialogButtonBox.Reset
        buttonBox   = QDialogButtonBox(buttons, parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


        layout = NGrid(self)

        layout.addWidget(QLabel(probeKey, self), 0,0)
        layout.addWidget(form,      1,0)
        layout.addWidget(doc,       1,1)
        layout.addWidget(sim,       2,0,1,2)
        layout.addWidget(buttonBox, 3,0,1,2)
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
        docBox  = QGroupBox(self)
        docBox.setTitle(self.tr('Manual'))
        docLayout = NGrid(docBox)
        docLayout.addWidget(QTextEdit(docBox))
        docBox.setLayout(docLayout)
        return docBox

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
        optionalFormLayout = QFormLayout(optionalBox)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'optional':
                optionalFormLayout.addRow('-%s' % pdef, QLineEdit(self))

        informationalBox = QGroupBox(self)
        informationalBox.setTitle(self.tr('Informational flags'))
        informationalFormLayout = QFormLayout(informationalBox)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'informational':
                informationalFormLayout.addRow('-%s' % pdef, QLineEdit(self))

        formFrame = NFrameContainer(self)
        formLayout = NGridContainer(formFrame)
        formLayout.addWidget(mandatoryBox,      0,0)
        formLayout.addWidget(optionalBox,       1,0)
        formLayout.addWidget(informationalBox,  2,0)
        formFrame.setLayout(formLayout)
        
        return formFrame





