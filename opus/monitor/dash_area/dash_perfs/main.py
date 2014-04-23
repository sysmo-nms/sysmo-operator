from    PySide.QtGui        import QTreeWidget
from    noctopus_widgets    import NFrameContainer, NGridContainer

class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(PerfTree(self), 0,0)
        self.setLayout(self._grid)

class PerfTree(QTreeWidget):
    def __init__(self, parent):
        super(PerfTree, self).__init__(parent)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr('Elements'), self.tr('Performances')])
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)

    def dropEvent(self, event):
        print "jojo", event.proposedAction()
