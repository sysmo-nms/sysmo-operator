from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorProxyEvents  import ChannelHandler

class AbstractChannelQFrame(QFrame):
    def __init__(self, parent, channel):
        super(AbstractChannelQFrame, self).__init__(parent)
        self.__channel = channel
        self.__connectProbe()

    def __connectProbe(self):
        ChannelHandler.singleton.subscribe(self, self.__channel)

    def handleProbeEvent(self, msg): 
        print self, ":you should handle this message: ", msg['msgType']

    def __disconnectProbe(self):
        ChannelHandler.singleton.unsubscribe(self, self.__channel)

    def destroy(self):
        self.__disconnectProbe()
        QFrame.destroy(self)
