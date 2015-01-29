from PyQt5.QtCore import (
    QObject,
    QSettings,
    pyqtSignal
)
from PyQt5.QtGui import (
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QFrame,
    QSpinBox
)

from noctopus_widgets import (
    NGrid,
    NFrameContainer,
    NGridContainer
)

import nocapi

class DocConfigurator(QDialog):
    def __init__(self, parent=None):
        super(DocConfigurator, self).__init__(parent)
        self.setWindowTitle('Documentation engine configurator')
        self.setWindowIcon(nocapi.nGetIcon('list-add'))
        dialogButtons = QDialogButtonBox(self)
        save = QPushButton('Save', self)
        save.setIcon(nocapi.nGetIcon('document-save'))
        dialogButtons.addButton(save,    QDialogButtonBox.AcceptRole)
        cancel = QPushButton('Cancel', self)
        cancel.setIcon(nocapi.nGetIcon('process-stop'))
        dialogButtons.addButton(cancel,  QDialogButtonBox.RejectRole)
        dialogButtons.accepted.connect(self.accept)
        dialogButtons.rejected.connect(self.reject)

        config      = NFrameContainer(self)
        configLay   = QFormLayout(self)
        config.setLayout(configLay)
        #engine = QComboBox(self)
        #engine.addItem('Standard Wiki')
        #engine.addItem('Noctopus advanced wiki')
        #engine.setEnabled(False)

        proto = QComboBox(self)
        proto.addItem('http')
        proto.addItem('https')

        port = QSpinBox(self)
        port.setValue(80)

        host = QLineEdit(self)
        host.setText('www.wikipedia.org')

        root = QLineEdit(self)
        root.setText('/wiki/')

        #sep = QFrame(self)
        #sep.setFrameShape(QFrame.HLine)
        #sep.setFrameShadow(QFrame.Sunken)
        configLay.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        #configLay.addRow('Doc engine:', engine)
        #configLay.addRow(sep)
        configLay.addRow('Protocol',    proto)
        configLay.addRow('Host:',       host)
        configLay.addRow('Port',        port)
        configLay.addRow('Root path:',  root)

        image = QLabel(self)
        image.setPixmap(nocapi.nGetPixmap('document-stack'))

        grid = NGrid(self)
        grid.addWidget(config,          0,1)
        grid.addWidget(dialogButtons,   1,1)
        grid.addWidget(image,           0,0,1,1)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,0)
        self.setLayout(grid)

        self.exec_()

        
