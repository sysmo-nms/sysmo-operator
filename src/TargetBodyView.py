from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    TargetProbeView import ProbeView
import  TkorderIcons
import  ModTracker


class TargetView(QFrame):
    
    " switch events from ModTrackerTarget based on the probe id "

    def __init__(self, parent, targetName):
        super(TargetView, self).__init__(parent)
        head        = QLabel(targetName, self)
        
        signalReceiver = self
        bodyScroll  = BodyScroll(self, targetName, signalReceiver)
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(head,        0, 0)
        grid.addWidget(bodyScroll,  1, 0)
        self.setLayout(grid)

    def setSignal(self, signalObj):
        signalObj.signal.connect(self.handleEvent)

    def setEmiters(self, emiters):
        self.probes = emiters

    def handleEvent(self, msg):
        probeId = msg['value']['id']
        self.probes[probeId].signal.emit(msg)

class BodyScroll(QScrollArea):
    def __init__(self, parent, targetName, signalReceiver):
        super(BodyScroll, self).__init__(parent)
        #self.setStyleSheet("QScrollArea { background: #FF0000 }")
        self.setWidgetResizable(True)
        lab = BodyFrame(self, targetName, signalReceiver)
        self.setWidget(lab)

class BodyFrame(QFrame):
    def __init__(self, parent, targetName, ancestor):
        super(BodyFrame, self).__init__(parent)
        probes      = dict()
        grid        = QGridLayout()
        targetDict  = ModTracker.TrackerMain.singleton.targets[targetName]
        # TODO look how to include palette() color return to a stylesheet
        #pal = self.palette()
        #col = pal.color(QPalette.Base)
        #(r,g,b,s)   = col.toTuple()

        print type(self)
        # TODO look how to apply stylesheet only to one element,
        #self.setObjectName('bodyFrame')
        #self.setStyleSheet('BodyFrame#bodyFrame {background:white;}')

        for probeId in targetDict:
            # create the probe widget
            pview  = ProbeView(self, targetName, probeId, targetDict[probeId]) 
            # create the signal
            signal = Communicate(self)
            # link the view to the signal
            pview.setSignal(signal)
            # save all this in a dict used to switch messages
            probes[probeId] = signal
            # grid the widget
            grid.addWidget(pview, probeId, 0)

        ancestor.setEmiters(probes)
        self.setLayout(grid)



class Communicate(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(Communicate, self).__init__(parent)
