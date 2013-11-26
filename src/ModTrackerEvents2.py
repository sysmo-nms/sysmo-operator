from    PySide.QtCore   import *


class TrackerEvents(QObject):
    
    " This class handle other widgets subscription and emit message "
    " received by the server with Signal(). The method 'handleMSG' receive "
    " messages from the server "
    " She is also responsible of the channel group concept and max channel "
    " limitations."

    def __init__(self, parent, maxChans=3):
        super(TrackerEvents, self).__init__(parent)
        TrackerEvents.singleton = self
        self.signalDict         = dict()
        defaultSignals          = ['probeInfo', 'targeInfo', 'probeModInfo']
        for sig in defaultSignals:
            self.signalDict[sig] = TrackerSignal(self)

    def handleMSG(self): pass

class TrackerSignal(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(TrackerSignal, self).__init__(parent)
