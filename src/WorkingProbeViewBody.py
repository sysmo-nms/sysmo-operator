from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    LoggerViewText      import TextLog
from    LoggerViewRrds      import *
from    CustomButtons       import *
from    LoggerViewEventsTimeLine    import *
from    LoggerViewEventsTimeLineSimple    import *

import  TkorderIcons


# class ProbeBody(QFrame):
#     def __init__(self, parent, viewType, probeDict):
#         super(ProbeBody, self).__init__(parent)
#         # body 
#         self.probeDict = probeDict
#         self.setFrameShape(QFrame.StyledPanel)
#         self.setFrameShadow(QFrame.Sunken)
#         grid   = QGridLayout(self)
#         self.eventsView = EventsView(self)
#         self.textLog    = TextLog(self)
#         grid.addWidget(self.eventsView, 0, 0)
#         grid.addWidget(self.textLog,   1, 0)
#         if viewType == 'text_and_rrdgraph':
#             self.rrdArea    = RrdArea(self, self.probeDict)
#             grid.addWidget(self.rrdArea, 2,0)
#         else:
#             self.rrdArea = None
# 
#         self.setLayout(grid)
# 
#     def handleProbeEvent(self, msg):
#         msgType = msg['msgType']
#         if msgType == 'probeDump':
#             if msg['logger'] == 'btracker_logger_text':
#                 self.textLog.textDump(msg['data'])
#             elif msg['logger'] == 'btracker_logger_rrd':
#                 self.rrdArea.rrdDump(msg['data'])
#             elif msg['logger'] == 'tracker_events':
#                 print "logger tracker_events event"
# 
#         elif msgType == 'probeReturn':
#             # log text
#             self.textLog.textAppend(msg['value'])
#             # rrd
#             if self.rrdArea != None: 
#                 self.rrdArea.updateGraph()
class ProbeBody(QTabWidget):
    def __init__(self, parent, viewType, probeDict):
        super(ProbeBody, self).__init__(parent)
        self.probeDict = probeDict

        self.setTabPosition(QTabWidget.West)
        self.setTabShape(QTabWidget.Triangular)
        self.setMinimumHeight(300)

        self.eventsView = EventsView(self)
        self.addTab(self.eventsView, 'Events')
        self.textLog    = TextLog(self)
        self.addTab(self.textLog, 'Text logs')
        if viewType == 'text_and_rrdgraph':
            self.rrdArea    = RrdArea(self, self.probeDict)
            self.addTab(self.rrdArea, 'RRDs')
        else:
            self.addTab(QFrame(self), 'RRDs')
            self.setTabEnabled(2, False)
            self.rrdArea = None

    def handleProbeEvent(self, msg):
        msgType = msg['msgType']
        if msgType == 'probeDump':
            if msg['logger'] == 'btracker_logger_text':
                self.textLog.textDump(msg['data'])
            elif msg['logger'] == 'btracker_logger_rrd':
                self.rrdArea.rrdDump(msg['data'])
            #elif msg['logger'] == 'tracker_events':
                #print "logger tracker_events event"

        elif msgType == 'probeReturn':
            # log text
            self.textLog.textAppend(msg['value'])
            # rrd
            if self.rrdArea != None: 
                self.rrdArea.updateGraph()
