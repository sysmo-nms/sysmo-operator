from pipe import Rrd4jSimple
from pipe import Rrd4jAsync
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys



class MyWidget(QWidget):
    def __init__(self,parent=None):
        super(MyWidget, self).__init__(parent)
        button = QPushButton(self)
        button.clicked.connect(self._ccc)
        self._rrd = Rrd4jAsync()
    
    def _ccc(self):
        print("hello ccc")
        sys.stdout.flush()
        self._rrd.execute("hello")
        print("hello ccc")
        sys.stdout.flush()
        self._rrd.execute("hello")


app = QApplication(sys.argv)
#r = Rrd4jAsync()
#r.execute("lkj")
#r.execute("lkqsdfqj")
#r.execute("aaabbc")
wid = MyWidget()
wid.show()
sys.exit(app.exec_())
