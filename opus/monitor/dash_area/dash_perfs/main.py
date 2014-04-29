from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    QLabel
)
from    opus.monitor.dash_area.dash_widgets import DashTreeWidget
from    opus.monitor.proxy  import AbstractChannelWidget
import  opus.monitor.api    as monapi

class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        dashWidget = DashTreeWidget(self)
        dashWidget.setDashLabels('Elements', 'RRDs logs')
        dashWidget.setItemWidgetClass(RrdLog)
        self._grid.addWidget(dashWidget, 0,0)
        self.setLayout(self._grid)

class RrdLog(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdLog, self).__init__(parent, probe)
        self._grid = NGridContainer(self)
        self.setLayout(self._grid)
        self._rrdElements = dict()

        self.probeName  = probe
        probes          = monapi.getProbesDict()
        self._probeConf = probes[probe]

        if 'bmonitor_logger_rrd' in self._probeConf['loggers'].keys():
            self._continue()
        else:
            self._cancel()

    def _continue(self):
        rrdConf = self._probeConf['loggers']['bmonitor_logger_rrd']
        for rrdname in rrdConf.keys():
            rrdconf = rrdConf[rrdname]
            self._rrdElements[rrdname] = RrdElement(self, rrdname, rrdconf)
            self._grid.addWidget(self._rrdElements[rrdname])
        self.connectProbe()
        self.goOn = True

    def _cancel(self):
        self.goOn = False

    def handleProbeEvent(self, msg):
        if msg['msgType'] == 'probeDump':
            if msg['logger'] == 'bmonitor_logger_rrd':
                print "rrd dump: ", msg['data']
        elif msg['msgType'] == 'probeReturn':
            print "probe return"

class RrdElement(NFrameContainer):
    def __init__(self, parent, rrdname, rrdconf):
        super(RrdElement, self).__init__(parent)
        self._rrdname = rrdname
        self._rrdconf = rrdconf
        self._grid = NGridContainer(self)
        self._grid.addWidget(QLabel(rrdname, self))
        self.setLayout(self._grid)

















