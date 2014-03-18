#!/usr/bin/env python2
from    PySide.QtGui        import (
    QDialog,
    QLineEdit,
    QSpinBox,
    QDialogButtonBox,
    QPushButton,
    QFrame,
    QFormLayout,
    QGridLayout
)
from    PySide.QtSvg        import QSvgWidget
from    NoctopusImages      import getImage, getIcon

class LogIn(QDialog):
    def __init__(self, callback, parent=None):
        super(LogIn, self).__init__(parent)
        self.setMinimumWidth(500)
        self.callback = callback


        # dev shortcuts
        autoName    = 'admuser'
        autoPass    = 'passwd'
        autoPort    = 8888
        autoHost    = 'localhost'


        # edit area
        self.nameLineEdit   = QLineEdit(self)
        self.nameLineEdit.setText(autoName)

        self.passLineEdit   = QLineEdit(self)
        self.passLineEdit.setEchoMode(QLineEdit.Password)
        self.passLineEdit.setText(autoPass)

        self.serverLineEdit = QLineEdit(self)
        self.serverLineEdit.setText(autoHost)

        self.serverPortEdit = QSpinBox(self)
        self.serverPortEdit.setRange(1, 65535)
        self.serverPortEdit.setValue(autoPort)

        formFrame   = QFrame(self)
        formLayout  = QFormLayout(formFrame)
        formLayout.addRow(self.tr("&Name:"),        self.nameLineEdit)
        formLayout.addRow(self.tr("&Password:"),    self.passLineEdit)
        formLayout.addRow(self.tr("&Server:"),      self.serverLineEdit)
        formLayout.addRow(self.tr("&Port:"),        self.serverPortEdit)
        formFrame.setLayout(formLayout)


        # button area
        ok = QPushButton(
            getIcon('applications-development'),
            self.tr("&Engage"),
            self)
        ok.setDefault(True)
        ok.clicked.connect(self.tryValidate)

        ko = QPushButton(
            getIcon('process-stop'),
            self.tr("&Abort"),
            self)
        ko.clicked.connect(self.close)

        helpB = QPushButton(
            getIcon('dialog-information'),
            self.tr("&Help"),
            self)
        helpB.setEnabled(False)

        buttons = QDialogButtonBox(self)
        buttons.addButton(ok,   QDialogButtonBox.RejectRole)
        buttons.addButton(ko,   QDialogButtonBox.ApplyRole)
        buttons.addButton(helpB,QDialogButtonBox.HelpRole)


        # graphic area
        svgImage = QSvgWidget(getImage('weather-showers'), self)
        svgImage.setFixedSize(150, 150)


        # LAYOUT
        grid = QGridLayout(self)
        grid.addWidget(formFrame,   0,1)
        grid.addWidget(svgImage,    0,0)
        grid.addWidget(buttons,     1,0,1,2)
        self.setLayout(grid)


    def tryValidate(self):
        tryDict = dict()
        tryDict['name']     = self.nameLineEdit.text()
        tryDict['pass']     = self.passLineEdit.text()
        tryDict['server']   = self.serverLineEdit.text()
        tryDict['port']     = self.serverPortEdit.value()

        ret = self.callback(tryDict)

        if ret == False:
            print "problem with connect"
        else:
            self.close()
