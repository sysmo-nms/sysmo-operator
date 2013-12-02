from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorProxyEvents  import ChannelHandler

class AbstractProbeView(QFrame):
    def __init__(self, parent):
        super(AbstractProbeView, self).__init__(parent)

    def disconnectProbe(self, probe):
        ChannelHandler.singleton.unsubscribe(self, probe)

    def connectProbe(self, probe):
        ChannelHandler.singleton.subscribe(self, probe)

    def handleProbeEvent(self, msg): 
        print self, ":you should handle this message: ", msg['msgType']
