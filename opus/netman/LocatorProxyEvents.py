from    PyQt5.QtCore   import *
import  Supercast

class ChannelHandler(QObject):
    
    def __init__(self, parent, maxChans=3):
        super(ChannelHandler, self).__init__(parent)
        ChannelHandler.singleton = self
        self.sc         = Supercast.Link.singleton
        self.sc.setMessageProcessor('modLocatorPDU', self.handleMsg)
        self.masterChan = 'locator-MasterChan'
        
    def handleMsg(self, msg): pass
