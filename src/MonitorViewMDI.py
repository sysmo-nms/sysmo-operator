from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorViewAbstract import AbstractProbeView

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class MDIView(AbstractProbeView):
    def __init__(self, parent):
        super(MDIView, self).__init__(parent)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(Controls(self), 0,0)
        grid.addWidget(MDIArea(self),  1,0)
        self.setLayout(grid)

class MDIArea(QMdiArea):
    def __init__(self, parent):
        super(MDIArea, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        test    = QLabel('hello mdiiiiiii', self)
        test2   = QLabel('hello mdiiiiiiiii', self)
        sub     = self.addSubWindow(test)
        sub2    = self.addSubWindow(test2)
        sub.setWindowTitle('test')
        sub2.setWindowTitle('test2')
        sub.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)
        sub2.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)
