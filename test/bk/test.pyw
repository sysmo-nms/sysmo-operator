#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Apr 18 11:20:33 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 300)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.vLabel     = MyLabel()
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.vLabel    , 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 18))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuHello = QtGui.QMenu(self.menuBar)
        self.menuHello.setObjectName(_fromUtf8("menuHello"))
        MainWindow.setMenuBar(self.menuBar)

        self.leftSelector = QtGui.QToolBar(MainWindow)
        self.leftSelector.setMovable(False)
        self.leftSelector.setOrientation(QtCore.Qt.Vertical)
        self.leftSelector.setAllowedAreas(QtCore.Qt.LeftToolBarArea)
        self.leftSelector.setObjectName(_fromUtf8("leftSelector"))
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.leftSelector)

        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.actionSdfsdf = QtGui.QAction(MainWindow)
        self.actionSdfsdf.setObjectName(_fromUtf8("actionSdfsdf"))
        self.actionQsdf = QtGui.QAction(MainWindow)
        self.actionQsdf.setObjectName(_fromUtf8("actionQsdf"))
        self.menuHello.addAction(self.actionSdfsdf)
        self.menuHello.addAction(self.actionQsdf)
        self.menuBar.addAction(self.menuHello.menuAction())

        self.leftSelector.addAction(self.actionSdfsdf)
        self.leftSelector.addAction(self.actionQsdf)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", 
            "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", 
            "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHello.setTitle(QtGui.QApplication.translate("MainWindow", 
            "hello", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSdfsdf.setText(QtGui.QApplication.translate("MainWindow", 
            "sdfsdf", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQsdf.setText(QtGui.QApplication.translate("MainWindow", 
            "qsdf*", None, QtGui.QApplication.UnicodeUTF8))


class MyLabel(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MyLabel, self).__init__(parent)
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.black)
        painter.translate(20, 100)
        painter.rotate(-90)
        painter.drawText(0, 0, "hellos")
        painter.end()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    #ui = MyLabel()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

