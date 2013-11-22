from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    PySide.QtSvg    import *
from    PySide.QtWebKit import *
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile

class RrdView(QLabel):
    def __init__(self, parent, probeDict):
        super(RrdView, self).__init__(parent)
        self.setStyleSheet("QFrame { background: #999999 }")
        self.setMinimumWidth(600)
        self.knownHeight    = 0
        self.knownWidth     = 0
        self.probeDict      = probeDict

        # tmp rrd file
        self.rrdDbFile      = QTemporaryFile()
        self.rrdDbFile.open()
        self.rrdDbFile.close()
        self.rrdDbFileName  = self.rrdDbFile.fileName()

        # tmp png file
        self.rrdGraphFile       = QTemporaryFile()
        self.rrdGraphFile.open()
        self.rrdGraphFile.close()
        self.rrdGraphFileName   = self.rrdGraphFile.fileName()

        # rrd conf
        self.rrdUpdateString = self.probeDict['loggers']['btracker_logger_rrd']['update']
        self.rrdMacroBinds   = self.probeDict['loggers']['btracker_logger_rrd']['binds']
        rrdGraphConf         = self.probeDict['loggers']['btracker_logger_rrd']['graphs']
        self.rrdGraphConf    = re.sub('<FILE>', self.rrdDbFileName, rrdGraphConf[0])

    def resizeEvent(self, event):
        "from doc: No drawing need be (or should be) done inside this handler"
        #print "new size", event.size()
        #print "old size", event.oldSize()
        QLabel.resizeEvent(self, event)

    def paintEvent(self, event):
        #print "paint event"
        QLabel.paintEvent(self, event)

    def handleEvent(self, msg):
        if   msg['msgType'] == 'probeReturn': 
            self.updateRrdDb(msg)
        elif msg['msgType'] == 'probeDump':
            self.dumpRrdDb(msg)

    def dumpRrdDb(self, msg):
        probeId = self.probeDict['id']
        if msg['value']['logger'] == 'btracker_logger_rrd':
            if msg['value']['id'] == probeId:
                self.rrdDbFile.open()
                self.rrdDbFile.write(msg['value']['data'])
                self.rrdDbFile.close()
                self.updateGraph()

    def updateRrdDb(self, msg):
        cmLine  = self.rrdUpdateString
        keyVals = msg['value']['keyVals']
        macroB  = self.rrdMacroBinds

        for key in macroB.keys():
            if key in keyVals:
                macro = macroB[key]
                value = keyVals[key]
                try:
                    fvalue = float(value)
                    ivalue = int(fvalue)
                except ValueError:
                    try: 
                        ivalue = int(value)
                    except ValueError: return
                    
                cmLine = cmLine.replace(macro, str(ivalue))
            else:
                print "Missing key. I will not update the rrd database."
                return
        template    = re.findall(r'--template\s+[^\s]+',  cmLine)
        template    = re.sub(r'--template\s+', r'', template[0])
        rrdvalues   = re.findall(r'N:[^\s]+', cmLine)
        rrdvalues   = rrdvalues[0]
        ret = rrdtool.update(str(self.rrdDbFileName), 
            '--template', template, rrdvalues)
        self.updateGraph()

    def updateGraph(self):
        defs    = re.findall(r'DEF:[^\s]+', self.rrdGraphConf)
        lines   = re.findall(r'LINE[^\s]+', self.rrdGraphConf)

        size = self.size()
        rrdWidth  = size.width()
        rrdHeight = size.height()
        rrdStart  = 3600 

        # python rrdtool did not support list of DEFs or LINEs in the module
        # args. This lead to generate the function as string and evaluate
        # it with eval().
        cmd = "rrdtool.graph(str(self.rrdGraphFileName), \
            '--imgformat', 'PNG', \
            '--width', str(rrdWidth), \
            '--height', str(rrdHeight), \
            '--full-size-mode', \
            '--border', '0', \
            '--dynamic-labels', \
            '--slope-mode', \
            '--tabwidth', '40', \
            '--watermark', 'Watermark', \
            '--color', 'BACK#000000', \
            '--color', 'CANVAS#0000ff', \
            '--color', 'SHADEA#0000ff', \
            '--color', 'SHADEB#0000ff', \
            '--color', 'GRID#0000ff', \
            '--color', 'MGRID#0000ff', \
            '--color', 'FONT#0000ff', \
            '--color', 'AXIS#0000ff', \
            '--color', 'FRAME#0000ff', \
            '--color', 'ARROW#0000ff', \
            '--start', '-%i' % rrdStart, \
            '--end', 'now',"
        for i in range(len(defs)):
            cmd += "'%s'," % defs[i]
        for i in range(len(lines)):
            cmd += "'%s'," % lines[i]
        cmd = re.sub(r',$', ')\n', cmd)
        eval(cmd)
        picture = QPixmap(self.rrdGraphFileName)
        print "pict = ", picture.size()
        print "area = ", self.size()
        self.setPixmap(picture)














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
