from Pyside import QtCore, QtGui, QtNetwork

class ModTrackerFrame(QtGui.QFrame):
    def __init__(self, parent):
        super(ModTrackerFrame, self).__init__(parent)
        self.ahead      = parent
        self.tButton    = QtGui.QPushButton("hell")
        lGrid           = QtGui.QGridLayout(self)
        lGrid.addWidget(self.tButton, 0, 0)
        self.setLayout(lGrid)

    def handleMsg(msg):
        print "message is ", msg

def hello(i):
    print "hello"

print "llllllllllllllllllllll"
