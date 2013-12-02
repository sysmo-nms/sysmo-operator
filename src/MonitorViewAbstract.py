from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorProxyEvents  import ChannelHandler

class AbstractProbeView(QFrame):
    def __init__(self, parent):
        super(AbstractProbeView, self).__init__(parent)

    def destroyProbe(self, probe):
        print "destroy probe"

    def createProbe(self, probe):
        print "create probe"

    def handleDump(self, msg): 
        "must be implemented by a derived class to do something"
        pass

    def handleReturn(self, msg):
        "must be implemented by a derived class to do something"
        pass
