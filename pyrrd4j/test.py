from pipe import Rrd4jSimple
from pipe import Rrd4jAsync
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys

def pr(val):
    print(val)
    sys.stdout.flush()


class MyWidget(QWidget):
    def __init__(self,parent=None):
        super(MyWidget, self).__init__(parent)
        button = QPushButton(self)
        button.clicked.connect(self._ccc)
        self._rrd = Rrd4jAsync()
    
    def _ccc(self):
        command = dict()
        command['callback'] = self.callback
        command['msg'] = "jojo"
        pr("hello ccc" + command['msg'])
        self._rrd.execute(command)
        command['msg'] = "juju"
        pr("hello ccc" + command['msg'])
        self._rrd.execute(command)

    def callback(self, msg):
        pr("callback msg: " + str(msg))


app = QApplication(sys.argv)
#r = Rrd4jAsync()
#r.execute("lkj")
#r.execute("lkqsdfqj")
#r.execute("aaabbc")
wid = MyWidget()
wid.show()
sys.exit(app.exec_())
