from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorViewAbstract import AbstractProbeView
from    MonitorProxyEvents  import ChannelHandler
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
        mdiWindow.destroy()
        mdiWidget.destroy()
        del self.probeViews[probe]

    def createProbeView(self, probe):
        mdiInfo = self.mdiArea.addProbeView(probe)
        self.probeViews[probe] = mdiInfo
        
        

class MDIArea(QMdiArea):
    def __init__(self, parent):
        super(MDIArea, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def delProbeView(self, win):
        self.removeSubWindow(win)

    def addProbeView(self, probe):
        mdiWidget = MDIProbeView(self, probe)
        mdiWidget.setWindowTitle(probe)
        mdiWindow = self.addSubWindow(mdiWidget)
        mdiWindow.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint)
        mdiWindow.show()
        return (mdiWidget, mdiWindow)
        

class MDIProbeView(AbstractProbeView):
    def __init__(self, parent, probe):
        super(MDIProbeView, self).__init__(parent)
        self.probeName      = probe
        self.chanHandler    = ChannelHandler.singleton
        self.probeConfig    = self.chanHandler.probes[probe]
        target = self.probeConfig['target']
        self.targetConfig   = self.chanHandler.targets[target]

        self.connectProbe(probe)

        grid = QGridLayout(self)
        lab = QLabel(probe, self)
        grid.addWidget(lab, 0,0)
        self.setLayout(grid)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'btracker_logger_text':
                print "handle probeDump text", self.probeName
            elif msg['logger'] == 'btracker_logger_rrd':
                print "handle probeDump rrd", self.probeName
        elif msg['msgType'] == 'probeReturn':
            print "handle probeReturn", self.probeName

    def destroy(self):
        self.disconnectProbe(self.probeName)
        AbstractProbeView.destroy(self)
