from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile

class RrdView(QFrame):
    def __init__(self, parent, probeDict):
        super(RrdView, self).__init__(parent)
        self.setStyleSheet("QFrame { background: #999999 }")
        self.setMinimumWidth(600)
        self.knownHeight    = 0
        self.knownWidth     = 0
        self.probeDict      = probeDict
        self.rrdDbFile      = QTemporaryFile()

    def resizeEvent(self, event):
        "from doc: No drawing need be (or should be) done inside this handler"
        #print "new size", event.size()
        #print "old size", event.oldSize()
        QFrame.resizeEvent(self, event)

    def paintEvent(self, event):
        #print "paint event"
        QFrame.paintEvent(self, event)

    def handleEvent(self, msg):
        probeId = self.probeDict['id']
        if   msg['msgType'] == 'probeReturn': 
            return
        elif msg['msgType'] == 'probeDump':
            if msg['value']['logger'] == 'btracker_logger_rrd':
                if msg['value']['id'] == probeId:
                    self.rrdDbFile.open()
                    self.rrdDbFile.write(msg['value']['data'])
                    self.rrdDbFile.close()

#     def setGraphs(self, graphs, rrdDbPath):
#         self.graphD     = dict()
#         grid        = QGridLayout()
#         graphCount  = len(graphs)
#         for i in range(graphCount):
#             self.graphD[i] = RrdGraph(self, graphs[i], rrdDbPath)
#             grid.addWidget(self.graphD[i], 0,i,1,1)
#
#         self.setLayout(grid)
#         self.updateGeometry()
# 
#         for i in self.graphD.keys():
#             self.graphD[i].updateRrd()
# 
#     def resizeEvent(self, event):
#         QFrame.resizeEvent(self, event)
# 
# class RrdGraph(QFrame):
#     def __init__(self, parent, config, rrdDbPath):
#         super(RrdGraph, self).__init__(parent)
#         graphConf = dict()
# 
#         fd, path = tempfile.mkstemp('.png')
#         graphConf['path'] = path
# 
#         opts    = re.findall(r'--[^\s]+\s+[^\s]+',  config)
#         defsTmp = re.findall(r'DEF[^\s]+',          config)
#         lines   = re.findall(r'LINE[^\s]+',         config)
#         defs  = [s.replace('<FILE>', rrdDbPath) for s in defsTmp]
# 
#         for i in range(len(opts)):
#             [a, b] = opts[i].split(' ')
#             graphConf[a] = b
# 
#         graphConf['defs'] = list()
#         for i in range(len(defs)):
#             graphConf['defs'].append(defs[i])
# 
#         graphConf['lines'] = list()
#         for i in range(len(lines)):
#             graphConf['lines'].append(lines[i])
# 
#         self.rrdGraphConf = graphConf
#         self.grid = QGridLayout()
#         self.grid.setContentsMargins(0,0,0,0)
#         self.grid.setHorizontalSpacing(0)
#         self.grid.setVerticalSpacing(0)
#         self.setLayout(self.grid)
# 
#     def mousePressEvent(self,event): pass
# 
#     def updateRrd(self):
#         label = QLabel("ici graph", self)
#         label.setScaledContents(True)
#         self.grid.addWidget(label, 0,0)
#         
#     def resizeEvent(self, event):
#         c = self.rrdGraphConf
#         rrdtool.graph(c['path'],
#             '--start',      c['--start'],
#             '--end',        c['--end'],
#             '--imgformat',  'PNG',
#             '--width',      str(self.width() / 3),
#             '--height',     str(self.height()),
#             c['defs'],
#             c['lines'])
# 
#         label = QLabel(self)
#         label.setScaledContents(False)
#         label.setPixmap(QPixmap(QImage(c['path'])))
#         label.setStyleSheet("QLabel { background: #FF0000 }")
#         self.grid.addWidget(label, 0,0)
#         QFrame.resizeEvent(self, event)
# 
