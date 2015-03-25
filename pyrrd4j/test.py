from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys


import pipe




## __init__ api begin
def init(colorDict, parent=None):
    cfg = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
        colorDict['BACK'],
        colorDict['CANVAS'],
        colorDict['SHADEA'],
        colorDict['SHADEB'],
        colorDict['GRID'],
        colorDict['MGRID'],
        colorDict['FONT'],
        colorDict['FRAME'],
        colorDict['ARROW'],
        colorDict['XAXIS']
    )
    cmd = "CONFIG|" + cfg
    return pipe.Rrd4jAsync(parent, cmd)

def graph(graph, callback):
    cmd = "%s;%s;%s;%s;%s;%i;%i;%i;%i;" % (
        graph['title'],
        graph['name'],
        graph['vlabel'],
        graph['filenameRrd'],
        graph['filenamePng'],
        graph['spanBegin'],
        graph['spanEnd'],
        graph['width'],
        graph['height'])
    for g in graph['DS']:
        cmd += g
        cmd += '@'
    # remove last pipe character
    cmd = cmd[:-1]
    command = dict()
    command['string'] = 'GRAPH|' + cmd
    command['callback'] = callback
    print("command is" + cmd)
    pipe.Rrd4jAsync.singleton.execute(command)

def update(command, callback):
    command['string'] = 'UPDATE|' + command['string']
    call(command, callback)

def call(command, callback):
    command['callback'] = callback
    pipe.Rrd4jAsync.singleton.execute(command)
## __init__ api end




def pr(val):
    print(val)
    sys.stdout.flush()


class MyWidget(QWidget):
    def __init__(self,parent=None):
        super(MyWidget, self).__init__(parent)
        button = QPushButton(self)
        button.clicked.connect(self._ccc)
        colorDict = dict()
        colorDict['BACK'] = "#000000FF"
        colorDict['CANVAS'] = "#000000FF"
        colorDict['SHADEA'] = "#000000FF"
        colorDict['SHADEB'] = "#000000FF"
        colorDict['GRID'] = "#000000FF"
        colorDict['MGRID'] = "#000000FF"
        colorDict['FONT'] = "#000000FF"
        colorDict['FRAME'] = "#000000FF"
        colorDict['ARROW'] = "#000000FF"
        colorDict['XAXIS'] = "#FFFFFFFF"

        self._rrd = init(colorDict, self)
    
    def _ccc(self):
        graph2 = dict()
        graph2['title']  = "ICMP performances"
        graph2['name']   = "ICMPPerfs"
        graph2['vlabel'] = "Milliseconds"
        graph2['filenameRrd'] = "./test.rrd"
        graph2['filenamePng'] = "./test.png"
        graph2['spanBegin'] = -12000
        graph2['spanEnd']   = -1
        graph2['width']     = 300
        graph2['height']    = 100
        graph2['DS'] = list()
        graph2['DS'].append("MinRoundTrip,area,Minimum round trip,#FF0000,AVERAGE")
        graph2['DS'].append("MaxRoundTrip,area,Maximum round trip,#00FF00,AVERAGE")
        graph2['DS'].append("AverageRoundTrip,area,Average round trip,#0000FF,AVERAGE")

        graph(graph2, self.callback)

    def callback(self, msg):
        pr("callback msg: " + str(msg))

app = QApplication(sys.argv)
wid = MyWidget()
wid.show()
sys.exit(app.exec_())

