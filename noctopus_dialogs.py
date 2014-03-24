#!/usr/bin/env python2
from    PySide.QtGui        import (
    QDialog,
    QLineEdit,
    QSpinBox,
    QDialogButtonBox,
    QPushButton,
    QFormLayout,
    QCheckBox,
    QButtonGroup,
    QLabel
)
from    PySide.QtSvg        import QSvgWidget
from    noctopus_api        import nGetImage, nGetIcon, nGetProxySettings
from    noctopus_widgets    import NFrame, NGrid

class Proxy(QDialog):
    def __init__(self, callback, parent=None):
        super(Proxy, self).__init__(parent)
        self._callback = callback
        self._initLayout()
        self._initState()

        self.show()

    def _initState(self):
        proxySet = nGetProxySettings()
        host = proxySet['host']
        port = proxySet['port']
        self.serverLineEdit.setText(host)
        self.portLineEdit.setValue(port)
        if proxySet['use'] == False:
            self.checkBoxNoProxy.setChecked(True)
        else:
            self.checkBoxProxy.setChecked(True)
            self.bottomFrame.setEnabled(True)
        
    def _initLayout(self):
        layout = NGrid(self)
        self._initCheckFrame()
        self._initFormFrame()
        self._initButtonFrame()
        layout.addWidget(self.topFrame,     0,0)
        layout.addWidget(self.bottomFrame,  1,0)
        layout.addWidget(self.buttonBox,    2,0)
        self.setLayout(layout)

    def _initCheckFrame(self):
        topFrame = NFrame(self)
        layout = NGrid(topFrame)

        self.checkBoxNoProxy = QCheckBox('No Proxy', self)
        self.checkBoxNoProxy.setChecked(True)
        self.checkBoxProxy   = QCheckBox('Manual proxy configuration', self)

        checkBoxGroup = QButtonGroup(self)
        checkBoxGroup.buttonClicked.connect(self.clicked)
        checkBoxGroup.setExclusive(True)
        checkBoxGroup.addButton(self.checkBoxProxy)
        checkBoxGroup.addButton(self.checkBoxNoProxy)

        layout.addWidget(self.checkBoxNoProxy,   0,0)
        layout.addWidget(self.checkBoxProxy,     1,0)
        layout.setColumnStretch(0,0)
        layout.setColumnStretch(1,0)
        layout.setColumnStretch(2,1)
        topFrame.setLayout(layout)
        self.topFrame = topFrame
    
    def clicked(self, arg):
        if self.checkBoxNoProxy.isChecked():
            self.bottomFrame.setDisabled(True)
        else:
            self.bottomFrame.setDisabled(False)

    def _initFormFrame(self):
        bottomFrame = NFrame(self)

        self.serverLineEdit = QLineEdit(self)
        self.portLineEdit   = QSpinBox(self)
        self.portLineEdit.setMinimum(1)
        self.portLineEdit.setMaximum(65535)

        layout = NGrid(bottomFrame)
        layout.addWidget(QLabel("Proxy server: ", self),   0,0)
        layout.addWidget(self.serverLineEdit,            0,1)
        layout.addWidget(QLabel("Port: ", self),    0,2)
        layout.addWidget(self.portLineEdit,              0,3)

        bottomFrame.setLayout(layout)
        bottomFrame.setDisabled(True)
        self.bottomFrame = bottomFrame
        

    def _initButtonFrame(self):
        # button area
        ok = QPushButton(
            nGetIcon('applications-development'),
            self.tr("&Validate"),
            self)
        ok.setDefault(True)
        ok.clicked.connect(self._validate)

        ko = QPushButton(
            nGetIcon('process-stop'),
            self.tr("&Abort"),
            self)
        ko.clicked.connect(self.close)

        helpB = QPushButton(
            nGetIcon('dialog-information'),
            self.tr("&Help"),
            self)
        helpB.setEnabled(False)

        buttons = QDialogButtonBox(self)
        buttons.addButton(ok,   QDialogButtonBox.RejectRole)
        buttons.addButton(ko,   QDialogButtonBox.ApplyRole)
        buttons.addButton(helpB,QDialogButtonBox.HelpRole)
        self.buttonBox = buttons

    def _validate(self):
        proxySet = dict()
        proxySet['use']     = self.checkBoxProxy.isChecked()
        proxySet['host']    = self.serverLineEdit.text()
        proxySet['port']    = self.portLineEdit.value()
        self._callback(proxySet)
        self.close()
