from    PySide.QtGui        import *
from    PySide.QtCore       import *

class Dash(QFrame):
    def __init__(self, parent):
        super(Dash, self).__init__(parent)
        self.dash   = DashTab(self)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.dash,           0,0)
        self.setLayout(grid)

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        self.stackDict  = dict()
        self.addTab(WorkView(self), 'Work view')
        self.addTab(MDIView(self), 'MDI view')

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class MDIView(QFrame):
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
        test    = QLabel('hello mdi', self)
        test2   = QLabel('hello mdi', self)
        sub     = self.addSubWindow(test)
        sub2    = self.addSubWindow(test2)
        sub.setWindowTitle('test')
        sub2.setWindowTitle('test2')
        sub.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)
        sub2.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)

class WorkView(QFrame):
    def __init__(self, parent):
        super(WorkView, self).__init__(parent)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(Controls(self), 0,0)
        grid.addWidget(WorkViewScroll(self), 1,0)
        self.setLayout(grid)

    def detach(self):
        print "workView detach"

    def fullScreen(self):
        print "workView fullscreen"

class WorkViewScroll(QScrollArea):
    def __init__(self, parent):
        super(WorkViewScroll, self).__init__(parent)
        self.setWidgetResizable(True)
        self.setWidget(WorkViewList(self))

class WorkViewList(QFrame):
    def __init__(self, parent):
        super(WorkViewList, self).__init__(parent)
        self.setBackgroundRole(QPalette.Dark)
        grid = QGridLayout(self)
        grid.addWidget(QLabel('scroll', self), 0,0)
        self.setLayout(grid)

class Detached(QDialog):
    def __init__(self, parent):
        super(Detached, self).__init__(parent)
        self.setModal(False)
        grid = QGridLayout(self)
        grid.addWidget(DashTab(self), 0,0)
        self.setLayout(grid)
        self.setWindowFlags(Qt.Window)
