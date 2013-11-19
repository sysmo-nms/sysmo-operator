from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile

class ProbeView(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeView, self).__init__(parent)

        self.vardir  = ModTracker.TrackerMain.singleton.vardir
        self.probeConf = probeDict
        loggers = probeDict['loggers']
        if 'btracker_logger_text' in loggers and \
           'btracker_logger_rrd' in loggers:
            viewType = 'full'
        elif 'btracker_logger_text' in loggers:
            viewType = 'text'
        elif 'btracker_logger_rrd'  in loggers:
            viewType = 'rrd'

        self.setFrameStyle(1)
        self.setFrameShadow(QFrame.Sunken)
        self.infoLabel  = ProbeInfos(self, targetName, probeId, probeDict)

        if viewType == 'full' or viewType == 'text':
    
            self.logArea    = QTextEdit(self)
            dtext   = QTextDocument()
            dtext.setMaximumBlockCount(500)
            tformat = QTextCharFormat()
            tformat.setFontPointSize(8.2)
            self.logArea.setDocument(dtext)
            self.logArea.setCurrentCharFormat(tformat)
            self.logArea.setReadOnly(True)
            self.logArea.setLineWrapMode(QTextEdit.NoWrap)
            if viewType == 'full':
                self.setFixedHeight(350)
                self.logArea.setFixedHeight(90)
                self.rrdButtons = ProbeButtons(self, probeDict)
                self.rrdGraphs  = ProbeGraphs(self, probeDict)
                grid = QGridLayout()
                grid.addWidget(self.infoLabel,   0,0,1,1)
                grid.addWidget(self.rrdButtons,  0,1,1,1)
                grid.addWidget(self.rrdGraphs,   0,2,1,1)
                grid.addWidget(self.logArea,     1,0,1,3)
                grid.setRowStretch(0,1)
                grid.setRowStretch(1,0)
                grid.setColumnStretch(0,0)
                grid.setColumnStretch(1,0)
                grid.setColumnStretch(2,1)
            else:
                "text only"
                self.setFixedHeight(200)
                grid = QGridLayout()
                grid.addWidget(self.infoLabel,   0,0,1,1)
                grid.addWidget(self.logArea,     0,1,1,1)
                grid.setRowStretch(0,1)
                grid.setColumnStretch(0,0)
                grid.setColumnStretch(1,1)
        else:
            "rrd only"
            self.setFixedHeight(260)
            self.rrdButtons = ProbeButtons(self, probeDict)
            self.rrdGraphs  = ProbeGraphs(self, probeDict)
            grid = QGridLayout()
            grid.addWidget(self.infoLabel,   0,0,1,1)
            grid.addWidget(self.rrdButtons,  0,1,1,1)
            grid.addWidget(self.rrdGraphs,   0,2,1,1)
            grid.setColumnStretch(0,0)
            grid.setColumnStretch(1,0)
            grid.setColumnStretch(2,1)
    
        self.setLayout(grid)

    def handleProbeReturn(self,msg):
        value   = msg['value']
        tstamp  = value['timestamp']
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        printable = string.replace('\n', ' ').replace('  ', ' ')
        self.logArea.append(time + "-> " + printable)
        #self.logArea.append(str(tstamp) + ">>>" + string)

    def handleProbeDump(self, msg):
        if msg['value']['logger'] == 'btracker_logger_text':
            self.btrackerLoggerTextDump(msg)
        else:
            self.btrackerLoggerRrdDump(msg)

    def btrackerLoggerTextDump(self, msg):
        # TODO format each timestamp to match the handleProbeReturn print
        self.logArea.append(str(msg['value']['data']).rstrip())

    def btrackerLoggerRrdDump(self, msg):
        chan    = msg['value']['channel']
        pid     = msg['value']['id']
        data    = msg['value']['data']

        rrdFile = os.path.join(self.vardir, chan + '-' + str(pid) + '.rrd')
        f       = open(rrdFile, 'wb')
        f.write(data)
        f.close()
        self.rrdFile = rrdFile
        self.graphRrds()

    def graphRrds(self):
        rrdFile     = self.rrdFile
        graphWidget = self.rrdGraphs
        confDict    = self.probeConf
        if 'btracker_logger_rrd' in confDict['loggers']:
            rrd_conf = confDict['loggers']['btracker_logger_rrd']
            rrd_graphs = rrd_conf['graphs']
        else: return
        if 'none' in rrd_graphs: return

        graphWidget.setGraphs(rrd_graphs, rrdFile)

class ProbeGraphs(QFrame):
    def __init__(self, parent, probeDict):
        super(ProbeGraphs, self).__init__(parent)
        self.lay = QGridLayout()

    def setGraphs(self, graphs, rrdDbPath):
        self.graphD     = dict()
        grid        = QGridLayout()
        graphCount  = len(graphs)
        for i in range(graphCount):
            self.graphD[i] = RrdGraph(self, graphs[i], rrdDbPath)
            grid.addWidget(self.graphD[i], 0,i,1,1)

        self.setLayout(grid)
        self.updateGeometry()

        for i in self.graphD.keys():
            self.graphD[i].updateRrd()

    def resizeEvent(self, event):
        QFrame.resizeEvent(self, event)

class RrdGraph(QFrame):
    def __init__(self, parent, config, rrdDbPath):
        super(RrdGraph, self).__init__(parent)
        graphConf = dict()

        fd, path = tempfile.mkstemp('.png')
        graphConf['path'] = path

        opts    = re.findall(r'--[^\s]+\s+[^\s]+',  config)
        defsTmp = re.findall(r'DEF[^\s]+',          config)
        lines   = re.findall(r'LINE[^\s]+',         config)
        defs  = [s.replace('<FILE>', rrdDbPath) for s in defsTmp]

        for i in range(len(opts)):
            [a, b] = opts[i].split(' ')
            graphConf[a] = b

        graphConf['defs'] = list()
        for i in range(len(defs)):
            graphConf['defs'].append(defs[i])

        graphConf['lines'] = list()
        for i in range(len(lines)):
            graphConf['lines'].append(lines[i])

        self.rrdGraphConf = graphConf
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.setLayout(self.grid)

    def mousePressEvent(self,event): pass

    def updateRrd(self):
        label = QLabel("ici graph", self)
        label.setScaledContents(True)
        self.grid.addWidget(label, 0,0)
        
    def resizeEvent(self, event):
        c = self.rrdGraphConf
        rrdtool.graph(c['path'],
            '--start',      c['--start'],
            '--end',        c['--end'],
            '--imgformat',  'PNG',
            '--width',      str(self.width() / 3),
            '--height',     str(self.height()),
            c['defs'],
            c['lines'])

        label = QLabel(self)
        label.setScaledContents(False)
        label.setPixmap(QPixmap(QImage(c['path'])))
        label.setStyleSheet("QLabel { background: #FF0000 }")
        self.grid.addWidget(label, 0,0)
        QFrame.resizeEvent(self, event)

class ProbeInfos(QFrame):
    def __init__(self, parent, targetName, probeId, probeDict):
        super(ProbeInfos, self).__init__(parent)
        self.setFixedWidth(200)
        status      = probeDict['status']
        inspectors  = probeDict['inspectors']
        loggers     = probeDict['loggers']
        active      = probeDict['active']
        step        = probeDict['step']
        timeout     = probeDict['timeout']
        probeId     = probeDict['id']
        probeMod    = probeDict['probeMod']
        infoType    = probeDict['infoType']
        name        = probeDict['name']
        perm        = probeDict['perm']
        properties  = probeDict['properties']

        grid = QGridLayout()
        grid.addWidget(QLabel('status: ' + status,  self),  0,0,1,1)
        grid.addWidget(QLabel('active: ' + str(active),  self),  1,0,1,1)
        grid.addWidget(QLabel('step: ' + str(step),  self),      2,0,1,1)
        grid.addWidget(QLabel('timeout: ' + str(timeout),  self), 3,0,1,1)
        grid.addWidget(QLabel('name: ' + name,  self),      4,0,1,1)
        grid.addWidget(QLabel('perm: ' + str(perm),  self),      5,0,1,1)
        grid.setRowStretch(50, 1)
        self.setLayout(grid)

class ProbeButtons(QFrame):
    def __init__(self, parent, probeDict):
        super(ProbeButtons, self).__init__(parent)
        self.setFrameShadow(QFrame.Sunken)
        self.setFrameStyle(1)
        grid = QGridLayout()
        grid.addWidget(QCheckBox('hour', self), 0,0,1,1)
        grid.addWidget(QCheckBox('day', self), 1,0,1,1)
        grid.addWidget(QCheckBox('month', self), 2,0,1,1)
        grid.addWidget(QCheckBox('year', self), 3,0,1,1)
        grid.addWidget(QCheckBox('5-year', self), 4,0,1,1)
        grid.setRowStretch(5,1)
        self.setLayout(grid)
