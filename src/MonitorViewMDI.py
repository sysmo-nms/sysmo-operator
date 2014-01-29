from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtWebKit     import *
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
from    LoggerViewRrds          import RrdArea
import  datetime
import  TkorderIcons

class Controls(QToolBar):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        de = QAction('Other', self)
        self.addAction(de)

class MDIView(QFrame):
    def __init__(self, parent):
        super(MDIView, self).__init__(parent)
        self.mdiArea = MDIArea(self)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(Controls(self), 0,0)
        grid.addWidget(self.mdiArea,   1,0)
        self.setLayout(grid)
        self.probeViews = dict()

    def deleteProbeView(self, probe):
        (mdiWidget, mdiWindow) = self.probeViews[probe]
        self.mdiArea.delProbeView(mdiWindow)
        self.mdiArea.tileSubWindows()
        mdiWindow.destroy()
        mdiWidget.destroy()
        del self.probeViews[probe]

    def createProbeView(self, probe):
        mdiInfo = self.mdiArea.addProbeView(probe)
        self.mdiArea.tileSubWindows()
        self.probeViews[probe] = mdiInfo
        
        

class MDIArea(QMdiArea):
    def __init__(self, parent):
        super(MDIArea, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.osmWidget = OSMView(self)
        self.osmWidget.setWindowTitle('OpenStreetMap view')
        osmWindow = self.addSubWindow(self.osmWidget)
        osmWindow.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)
        osmWindow.show()

    def delProbeView(self, win):
        self.removeSubWindow(win)

    def addProbeView(self, probe):
        mdiWidget = MDIProbeView(self, probe)
        mdiWidget.setWindowTitle(probe)
        mdiWindow = self.addSubWindow(mdiWidget)
        mdiWindow.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)
        mdiWindow.show()
        return (mdiWidget, mdiWindow)
        

class OSMView(QWebView):
    def __init__(self, parent):
        super(OSMView, self).__init__(parent)
        self.load(QUrl("./html/OpenStreetMap.html"))

class MDIProbeView(AbstractChannelQFrame):
    def __init__(self, parent, probe):
        super(MDIProbeView, self).__init__(parent, probe)
        self.probeName      = probe
        self.chanHandler    = ChannelHandler.singleton
        self.probeConfig    = self.chanHandler.probes[probe]
        target = self.probeConfig['target']
        self.targetConfig   = self.chanHandler.targets[target]

        # text view on all types of probes

        # cartouche
        #self.cartoucheArea = QLabel(probe, self)
        grid = QGridLayout(self)

        self.textArea   = None
        self.rrdArea    = None
        # if there is a rrd logger
        if 'btracker_logger_rrd' in self.probeConfig['loggers'].keys():
            self.rrdArea = RrdArea(self, self.probeConfig)
            grid.addWidget(self.rrdArea,  0,0,2,1)
            #grid.addWidget(self.cartoucheArea,  0,0,2,1)
            #grid.addWidget(self.textArea,       1,1,1,1)
            #grid.addWidget(self.rrdArea,        0,1,1,1)
            #grid.setRowStretch(1,0)
            #grid.setRowStretch(0,1)
        else:
            self.textArea   = QTextEdit(self)
            dtext           = QTextDocument()
            dtext.setMaximumBlockCount(500)
            tformat         = QTextCharFormat()
            tformat.setFontPointSize(8.2)
            self.textArea.setDocument(dtext)
            self.textArea.setCurrentCharFormat(tformat)
            self.textArea.setReadOnly(True)
            self.textArea.setLineWrapMode(QTextEdit.NoWrap)
            self.textArea.setFixedWidth(300)
            self.textArea.setFixedHeight(90)
            grid.addWidget(self.textArea,       0,0)

        self.setLayout(grid)
        self.connectProbe()

    def handleTextDump(self, data):
        self.textArea.append(str(data).rstrip())

    def handleReturn(self, value):
        tstamp  = value['timestamp'] / 1000000
        time    = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')
        string  = value['originalRep'].rstrip()
        printable = string.replace('\n', ' ').replace('  ', ' ')
        self.textArea.append(time + "-> " + printable)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'btracker_logger_text':
                if self.textArea != None:
                    for line in msg['data']:
                        self.textArea.append(str(line).rstrip())
            elif msg['logger'] == 'btracker_logger_rrd':
                if self.rrdArea != None: 
                    self.rrdArea.rrdDump(msg['data'])
        elif msg['msgType'] == 'probeReturn':
            if self.textArea != None:
                self.handleReturn(msg['value'])
            if self.rrdArea != None:
                self.rrdArea.updateGraph()
