from PySide import QtGui

class ModTracker(QtGui.QFrame):
    def __init__(self, parent):
        super(ModTracker, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        parent.setMessageProcessor('modTrackerPDU', self.handleMsg)
        self.initMainFrame()

    def initMainFrame(self):
        tButton = QtGui.QPushButton("hell", self)
        lGrid   = QtGui.QGridLayout(self)
        lGrid.addWidget(tButton, 0, 0)
        self.setLayout(lGrid)

    def handleMsg(self, msg):
        print "modTracker message is ", msg

def hello(iii):
    print "hello", iii
