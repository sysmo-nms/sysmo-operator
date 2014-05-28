from PySide.QtGui import (
    QDialog,
    QLabel,
    QFormLayout,
    QLineEdit
)

from noctopus_widgets import (
    NGrid,
    NGridContainer,
    NFrameContainer
)

class ProbeForm(QDialog):
    def __init__(self, probeDefs, probeKey, parent=None):
        super(ProbeForm, self).__init__(parent)
        self._probeDef  = probeDefs[probeKey]
        self._probeName = probeKey
        form   = self._generateForm()
        layout = NGrid(self)

        layout.addWidget(QLabel(probeKey, self), 0,0)
        layout.addWidget(form, 1,0)
        self.setLayout(layout)

    def _generateForm(self):
        formFrame = NFrameContainer(self)
        pdefs = self._probeDef['flags_def']
        formLayout = QFormLayout(formFrame)
        for pdef in pdefs.keys():
            formLayout.addRow(pdef, QLineEdit(self))

        formFrame.setLayout(formLayout)
        return formFrame
