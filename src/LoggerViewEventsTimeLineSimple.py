from    PySide.QtGui        import *
from    PySide.QtCore       import *

class SimpleTimeLine(QFrame):
    def __init__(self, parent):
        super(SimpleTimeLine, self).__init__(parent)
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        #status1 = QLabel('HEEEEEEEEELLLO', self)
        #status1.setFixedHeight(10)
        #status1.setFixedWidth(100)
        #status1.move(0,0)
        #status1.show()
        #grid = QGridLayout()
        a = QPushButton('simple time line', self)
        a.move(0,0)
        a.resize(100,100)
        a.show()
        #grid.addWidget(a, 0,0)
        #self.setLayout(grid)
