from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    MonitorAbstract     import AbstractChannelQFrame
from    MonitorProxyEvents  import ChannelHandler
from    LoggerViewEventsTimeLineSimple    import SimpleTimeLine
from    LoggerViewText              import TextLog
from    LoggerViewRrds              import *
from    WorkingProbeView            import ProbeView
from    WorkingTargetView           import TargetView

import  MonitorProxyEvents
import  TkorderIcons
import  os
import  datetime

class Controls(QFrame):
    def __init__(self, parent):
        super(Controls, self).__init__(parent)
        self.viewAll        = QPushButton('Complete', self)
        self.viewTimeline   = QPushButton('Status Timeline')
        self.viewRrd        = QPushButton('Performances', self)
        
        grid = QGridLayout(self)
        #grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.viewAll,        0,0)
        grid.addWidget(self.viewTimeline,   0,1)
        grid.addWidget(self.viewRrd,        0,2)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,1)

        self.setLayout(grid)


class WorkView(QFrame):
    def __init__(self, parent):
        super(WorkView, self).__init__(parent)

        self.tmpMainGridCount = 0
        self.targetViews = dict()

        self.completeView   = CompleteView(self)
        self.statusView     = StatusTimelineView(self)
        self.rrdPerfView    = RrdPerformancesView(self)


        self.tab = QTabWidget(self)
        self.tab.setTabPosition(QTabWidget.West)

        self.tab.addTab(self.completeView,  'Complete')
        self.tab.addTab(self.statusView,    'Status timeline')
        self.tab.addTab(self.rrdPerfView,   'Performances view')

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        #grid.addWidget(Controls(self), 0,0)
        grid.addWidget(self.tab, 1,0)
        self.setLayout(grid)

    def deleteProbeView(self, probe):
        t = MonitorProxyEvents.ChannelHandler.singleton.probes[probe]['target']
        r = self.targetViews[t].removeProbe(probe)
        if r == 'empty':
            self.completeView.grid.removeWidget(self.targetViews[t])
            self.targetViews[t].deleteLater()
            self.completeView.grid.update()
            del self.targetViews[t]

    def createProbeView(self, probe):
        # get the target from the probe
        t = MonitorProxyEvents.ChannelHandler.singleton.probes[probe]['target']
        # if not allready exist, create the target widget with probe as
        # argument
        self.statusView.createProbe(probe)

        if t in self.targetViews:
            self.targetViews[t].newProbe(probe)
        else:
            self.targetViews[t] = TargetView(self, t, probe)
            self.completeView.grid.addWidget(self.targetViews[t], self.tmpMainGridCount, 0)
            self.tmpMainGridCount += 1
            self.completeView.grid.setRowStretch(self.tmpMainGridCount, 0)
            self.completeView.grid.setRowStretch(self.tmpMainGridCount + 1, 1)
            self.completeView.grid.update()


##############################################################################
##############################################################################
class StatusTimelineView(QScrollArea):
    def __init__(self, parent):
        super(StatusTimelineView, self).__init__(parent)
        self.setWidgetResizable(True)
        self.grid = QGridLayout(self)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.fr   = QFrame(self)
        self.fr.setLayout(self.grid)
        self.setWidget(self.fr)
        self.widgetCount = 0

    def createProbe(self, probe):
        label = QLabel(probe,self)
        self.grid.addWidget(label,                              self.widgetCount,0)
        self.grid.addWidget(StatusTimelineElement(self, probe), self.widgetCount,1)
        self.grid.setRowStretch(self.widgetCount, 0)
        self.widgetCount += 1
        self.grid.setRowStretch(self.widgetCount, 1)
    
    def deleteProbe(self, probe): pass

class StatusTimelineElement(AbstractChannelQFrame):
    def __init__(self, parent, probe):
        super(StatusTimelineElement, self).__init__(parent, probe)
        grid = QGridLayout(self)
        self.timeLine = SimpleTimeLine(self)
        grid.addWidget(self.timeLine,       0,0)
        self.setLayout(grid)
        self.connectProbe()

    def handleProbeEvent(self, msg):
        self.timeLine.handleProbeEvent(msg)
##############################################################################
##############################################################################

class RrdPerformancesView(QLabel):
    def __init__(self, parent):
        super(RrdPerformancesView, self).__init__(parent)
        self.setText('perfs')

class RrdPerformancesElement(AbstractChannelQFrame):
    def __init__(self, parent, probe):
        super(RrdPerformancesView, self).__init__(parent, probe)
        self.setWidgetResizable(True)
        probeDict = MonitorProxyEvents.ChannelHandler.singleton.probes[probe]

        self.grid = QGridLayout(self)
        self.fr   = QFrame(self)
        self.fr.setLayout(self.grid)
        self.setWidget(self.fr)

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'btracker_logger_rrd':
                self.rrdArea.rrdDump(msg['data'])
        elif msg['msgType'] == 'probeReturn':
            self.rrdArea.updateGraph()
##############################################################################
##############################################################################

class CompleteView(QScrollArea):
    def __init__(self, parent):
        super(CompleteView, self).__init__(parent)
        self.setWidgetResizable(True)
        self.grid = QGridLayout(self)
        self.fr   = QFrame(self)
        self.fr.setLayout(self.grid)
        self.setWidget(self.fr)






