from PySide import QtGui
import ModTracker

class TkorderCentralWidget(QtGui.QFrame):
    def __init__(self, parent):
        super(TkorderCentralWidget, self).__init__(parent)

        layout      = QtGui.QGridLayout()
        modTracker  = ModTracker.ModTracker(self)
        layout.addWidget(modTracker, 0, 0)

        self.setLayout(layout)
