from    PySide.QtGui    import *
from    PySide.QtCore   import *
from    TargetProbeView import ProbeView
import  os
import  datetime
import  TkorderIcons
import  ModTracker
import  rrdtool
import  re
import  tempfile


class TargetView(QFrame):
    
    " switch events from ModTrackerTarget based on the probe id "

    def __init__(self, parent, targetName):
        super(TargetView, self).__init__(parent)
        head            = QLabel(targetName, self)
        (scrollFrame,)  = self.generateProbesFrame(targetName),
        
        bodyScroll  = QScrollArea(self)
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(head,        0, 0)
        grid.addWidget(bodyScroll,  1, 0)
        self.setLayout(grid)
        bodyScroll.setWidget(scrollFrame)

    def setSignal(self, signalObj):
        signalObj.signal.connect(self.handleEvent)

    def handleEvent(self, msg):
        probeId = msg['value']['id']
        self.probes[probeId].signal.emit(msg)

    def generateProbesFrame(self, targetName):
        self.probes = dict()
        grid = QGridLayout()

        targetDict = ModTracker.TrackerMain.singleton.targets[targetName]

        for probeId in targetDict:
            # create the probe widget
            pview  = ProbeView(self, targetName, probeId, targetDict[probeId]) 
            # create the signal
            signal = Communicate(self)
            # link the view to the signal
            pview.setSignal(signal)
            # save all this in a dict used to switch messages
            self.probes[probeId] = signal
            # grid the widget
            grid.addWidget(pview, probeId, 0)

        fr = QFrame(self)
        fr.setLayout(grid)
        return fr

class Communicate(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(Communicate, self).__init__(parent)
