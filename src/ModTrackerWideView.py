from    PySide      import QtGui, QtCore

class View(QtGui.QFrame):
    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.fr = QtGui.QLabel("WIDEVIEW")
        grid = QtGui.QGridLayout()
        grid.addWidget(self.fr, 0, 0)
        self.setLayout(grid)
