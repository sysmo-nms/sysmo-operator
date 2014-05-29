from PySide.QtGui import (
    QDialog,
    QLabel,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QPushButton
)

from noctopus_widgets import (
    NGrid,
    NGridContainer,
    NFrameContainer
)

class ProbeForm(QDialog):
    def __init__(self, probeDefs, probeKey, parent):
        super(ProbeForm, self).__init__(parent)
        self.setModal(True)
        self._caller    = parent
        self._probeDef  = probeDefs[probeKey]
        self._probeName = probeKey

        form        = self._generateForm()

        buttons     = QDialogButtonBox.Save|QDialogButtonBox.Cancel|QDialogButtonBox.Reset
        buttonBox   = QDialogButtonBox(buttons, parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


        layout = NGrid(self)

        layout.addWidget(QLabel(probeKey, self), 0,0)
        layout.addWidget(form,      1,0)
        layout.addWidget(QPushButton('Simulate', self), 2,0)
        d = QLineEdit(self)
        d.setText('> %s' % probeKey)
        layout.addWidget(d, 3,0)
        layout.addWidget(buttonBox, 4,0)


        self.setLayout(layout)

    def accept(self):
        print "aaaaaaaaaaaaaccept"
        QDialog.accept(self)
        
        
    def _generateForm(self):
        formFrame = NFrameContainer(self)
        pdefs = self._probeDef['flags_def']
        formLayout = QFormLayout(formFrame)
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'mandatory':
                formLayout.addRow('-%s' % pdef, QLineEdit(self))

        formLayout.addWidget(QLabel('optional', self))
        for pdef in pdefs.keys():
            if pdefs[pdef]['role'] == 'optional':
                formLayout.addRow('-%s' % pdef, QLineEdit(self))

        formFrame.setLayout(formLayout)
        return formFrame
