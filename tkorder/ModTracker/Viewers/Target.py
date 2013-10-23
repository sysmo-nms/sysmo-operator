from    PySide      import QtGui, QtCore
from    TkorderMain import *
import  TkorderIcons
import  Supercast


class Stack(QtGui.QStackedWidget):
    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.chanList       = None

    def setView(self, target, probeId):
        targetName      = target.data(QtCore.Qt.UserRole + 1)
        currentWidget   = self.widget(1)
        if currentWidget == None:
            self.insertWidget(1, ElementView(self, targetName, probeId))
        else:
            self.removeWidget(currentWidget)
            currentWidget.deleteLater()
            self.insertWidget(1, ElementView(self, targetName, probeId))
        self.setCurrentIndex(1)


class ElementView(QtGui.QFrame):
    def __init__(self, parent, targetName, probeId):
        super(ElementView, self).__init__(parent)
        self.fr = QtGui.QLabel(targetName)
        grid = QtGui.QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)
