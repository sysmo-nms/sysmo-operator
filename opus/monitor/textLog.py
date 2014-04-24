
class RrdAreaTest(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdAreaTest, self).__init__(parent, probe)
        logger = QTextEdit(self)
        logger.setTextInteractionFlags(Qt.NoTextInteraction)        
        logger.setFixedHeight(80)
        logger.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        logger.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        logger.setLineWrapMode(QTextEdit.NoWrap)
        self.logger = logger

        grid = QGridLayout(self)
        grid.addWidget(self.logger, 0,0)
        self.setLayout(grid)

        self.connectProbe()
    
    def handleProbeEvent(self, msg):
        print msg.keys()
        #print msg['logger']
        #print msg['msgType']
