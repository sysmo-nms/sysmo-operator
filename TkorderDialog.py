#!/usr/bin/env python2
from    PySide.QtCore       import *
from    PySide.QtGui        import *
from    PySide.QtSvg        import *
import  TkorderIcons
import  TkorderMain

class LogIn(QDialog):
    def __init__(self, parent=None):
        super(LogIn, self).__init__(parent)
        autoName    = 'admuser'
        autoPass    = 'passwd'
        autoPort    = 8888
        #autoHost    = 'localhost'
        autoHost    = '192.168.0.9'

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

        self.setMinimumWidth(500)

        buttons = QDialogButtonBox(self)
        ok = QPushButton(TkorderIcons.get('applications-development'), self.tr("&Engage"), self)
        ko = QPushButton(TkorderIcons.get('process-stop'), self.tr("&Abort"), self)
        helpB = QPushButton(TkorderIcons.get('dialog-information'), self.tr("&Help"), self)
        helpB.setEnabled(False)
        ok.setDefault(True)
        buttons.addButton(ok, QDialogButtonBox.RejectRole)
        buttons.addButton(ko, QDialogButtonBox.ApplyRole)
        buttons.addButton(helpB, QDialogButtonBox.HelpRole)
        ok.clicked.connect(self.tryValidate)
        ko.clicked.connect(self.close)

        formFrame   = QFrame(self)
        formLayout  = QFormLayout(formFrame)
        formLayout.addRow(self.tr("&Name:"),        self.nameLineEdit)
        formLayout.addRow(self.tr("&Password:"),    self.passLineEdit)
        formLayout.addRow(self.tr("&Server:"),      self.serverLineEdit)
        formLayout.addRow(self.tr("&Port:"),        self.serverPortEdit)
        formFrame.setLayout(formLayout)

        svgImage = QSvgWidget(TkorderIcons.getImage('weather-showers'), self)
        svgImage.setFixedSize(150, 150)
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

        ret = TkorderMain.TkorderClient.singleton.tryConnect(tryDict)
        if ret == False:
            print "problem with connect"
        else:
            self.close()

