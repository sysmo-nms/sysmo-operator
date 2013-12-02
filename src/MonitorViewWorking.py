from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorViewAbstract import AbstractProbeView

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class WorkView(AbstractProbeView):
    def __init__(self, parent):
        super(WorkView, self).__init__(parent)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(Controls(self), 0,0)
        grid.addWidget(WorkViewScroll(self), 1,0)
        self.setLayout(grid)

class WorkViewScroll(QScrollArea):
    def __init__(self, parent):
        super(WorkViewScroll, self).__init__(parent)
        self.setWidgetResizable(True)
        self.setWidget(WorkViewList(self))

class WorkViewList(QFrame):
    def __init__(self, parent):
        super(WorkViewList, self).__init__(parent)
        self.setBackgroundRole(QPalette.Base)
        grid = QGridLayout(self)
        grid.addWidget(QLabel('scroll area', self), 0,0)
        self.setLayout(grid)
