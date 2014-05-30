from PySide.QtGui import (
    QDialog,
    QLabel,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDialogButtonBox,
    QPushButton
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

        form        = self._generateForm()

        buttons     = QDialogButtonBox.Save|QDialogButtonBox.Cancel|QDialogButtonBox.Reset
        buttonBox   = QDialogButtonBox(buttons, parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


        layout = NGrid(self)

        layout.addWidget(QLabel(probeKey, self), 0,0)
        layout.addWidget(form,      1,0)
        self._simulateButton = QPushButton(self.tr('Simulate'), self)
        self._simulateButton.clicked.connect(self._simulateComm)
        layout.addWidget(self._simulateButton, 2,0)
        self._comm = QTextEdit(self)
        self._updateComm('none')
        layout.addWidget(self._comm, 3,0)
        layout.addWidget(buttonBox, 4,0)


        self.setLayout(layout)

    def accept(self):
        print "aaaaaaaaaaaaaccept"
        QDialog.accept(self)
        
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
        self._comm.setText(comm)
        
    def _generateForm(self):
        formFrame = NFrameContainer(self)
        pdefs = self._probeDef['flags_def']
        formLayout = QFormLayout(formFrame)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'mandatory':
                self._config[pdef] = QLineEdit(self)
                self._config[pdef].textChanged.connect(self._updateComm)
                formLayout.addRow('-%s' % pdef, self._config[pdef])

        formLayout.addWidget(QLabel('optional', self))
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'optional':
                formLayout.addRow('-%s' % pdef, QLineEdit(self))

        formFrame.setLayout(formLayout)
        return formFrame
