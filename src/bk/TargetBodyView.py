from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    TargetProbeView import ProbeView
import  TkorderIcons
import  ModTracker


class TargetView(QFrame):
    
    " switch events from ModTrackerTarget based on the probe id "

    def __init__(self, parent, targetName):
        super(TargetView, self).__init__(parent)
        
        signalReceiver = self
        head        = TargetHead(self, targetName, signalReceiver)
        bodyScroll  = BodyScroll(self, targetName, signalReceiver)
        grid = QGridLayout(self)
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

class TargetHead(QFrame):
    def __init__(self, parent, targetName, signalReceiver):
        super(TargetHead, self).__init__(parent)
        grid = QGridLayout(self)
        grid.addWidget(QLabel(targetName, self), 0,0)
        self.setLayout(grid)

class BodyScroll(QScrollArea):
    def __init__(self, parent, targetName, signalReceiver):
        super(BodyScroll, self).__init__(parent)
        self.setWidgetResizable(True)
        lab = BodyFrame(self, targetName, signalReceiver)
        self.setWidget(lab)

class BodyFrame(QFrame):
    def __init__(self, parent, targetName, ancestor):
        super(BodyFrame, self).__init__(parent)
        probes      = dict()
        grid        = QGridLayout(self)
        grid.setContentsMargins(5,5,5,5)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(5)

        targetDict  = ModTracker.TrackerMain.singleton.targets[targetName]

        backg = ModTracker.TrackerMain.singleton.colorDict2['Base']
        winbk = ModTracker.TrackerMain.singleton.colorDict2['Window']
        # TODO look how to apply stylesheet only to one element,
        #self.setObjectName('bodyFrame')
        #self.setStyleSheet('QFrame#bodyFrame {background:%s;}' % backg)
        # does not work

        self.setStyleSheet('QFrame {background: %s;}' % backg)

        for probeId in targetDict:
            # create the probe widget
            pview  = ProbeView(self, targetName, probeId, targetDict[probeId]) 
            # XXX overwrite setStyleSheet
            pview.setStyleSheet('QFrame {background: %s;}' % winbk)
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
