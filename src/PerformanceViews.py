from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtWebKit import *

class PerformanceMap(QFrame):
    def __init__(self, parent):
        super(PerformanceMap, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.osmView = QWebView(self)
        self.osmView.load(QUrl('./html/OpenStreetMap.html'))

        grid = QGridLayout(self)
        grid.addWidget(self.osmView, 0,0)
        grid.addWidget(QFrame(self), 0,0)
        self.setLayout(grid)
