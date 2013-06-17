from PySide import QtGui, QtCore
import TkorderMain

class ModTracker(QtGui.QSplitter):
    @classmethod
    def initTargetView(cls):
        cls.targetView = ''

    @classmethod
    def targetView(cls):
        return cls.targetView

    def __init__(self, parent):
        super(ModTracker, self).__init__(parent)

        " forward 'modTrackerPDU to me "
        sin = TkorderMain.SupercastClient.singleton
        sin.setMessageProcessor('modTrackerPDU', self.handleMsg)

        self.addWidget(LeftPane(self))
        self.addWidget(RightPane(self))

    def handleMsg(self, msg):
        print "modTracker message is ", msg


class LeftPane(QtGui.QFrame):
    @classmethod
    def setSingleton(cls, obj):
        cls.singleton = obj

    @classmethod
    def singleton(cls):
        return cls.singleton

    @classmethod
    def toggle(cls):
        if (cls.singleton.isHidden() == True):
            cls.singleton.show()
        else:
            cls.singleton.hide()


    def __init__(self, parent):
        super(LeftPane, self).__init__(parent)
        LeftPane.setSingleton(self)
        self.treeview   =  LeftPaneTree(self)
        self.button     =  QtGui.QPushButton("left here", self)
        grid = QtGui.QGridLayout()
        grid.addWidget(self.button,   0, 0)
        grid.addWidget(self.treeview, 1, 0)
        self.setLayout(grid)


class LeftPaneTree(QtGui.QTreeView):
    def __init__(self, parent):
        super(LeftPaneTree, self).__init__(parent)
        model = QtGui.QFileSystemModel()
        model.setRootPath(QtCore.QDir.currentPath())
        self.setModel(model)


class RightPane(QtGui.QFrame):
    # TODO stacked widget
    def __init__(self, parent):
        super(RightPane, self).__init__(parent)
        self.button      =  QtGui.QPushButton("toggle left")
        grid = QtGui.QGridLayout()
        grid.addWidget(self.button,   0, 0)
        self.setLayout(grid)
        self.connect(
            self.button,
            QtCore.SIGNAL("clicked()"),
            LeftPane.toggle
        )
