from    PyQt5.QtCore   import (
    QSettings,
    QSize,
    QTimeLine,
    pyqtSignal,
    Qt
)

from    PyQt5.QtGui    import (
    QPixmap,
    QIcon,
    QPalette,
    QFont
)

from    PyQt5.QtWidgets    import (
    QWidget,
    QDialog,
    QScrollArea,
    QStatusBar,
    QProgressBar,
    QPushButton,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QTabWidget
)

from    sysmo_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid,
    QLabel
)

from    monitor.proxy import AbstractChannelWidget, ChanHandler, NTempFile
from    monitor.windows.rrdarea  import RrdArea
import  monitor.api    as monapi
import  monitor.norrd  as norrd

import  sysmapi
import  pyrrd4j
import  platform
import  nchecks
import  re
import  os

def openPerformancesFor(probe, displayName):
    if probe in list(LoggerView.Elements.keys()):
        LoggerView.Elements[probe].show()
        return
    else:
        LoggerView.Elements[probe] = LoggerView(probe, displayName)

class LoggerView(QDialog):
    Elements = dict()
    def __init__(self, probe, displayName, parent=None):
        super(LoggerView, self).__init__(parent)

        self._statusBar = LogStatusBar(self)
        self._menus     = ProbeMenus(self)

        probeee = ChanHandler.singleton.probes[probe]
        loggers = list(ChanHandler.singleton.probes[probe]['loggers'].keys())
        rrdlogger   = False
        textlogger  = False
        eventlogger = False
        
        self._layout    = NGrid(self)
        self._layout.addWidget(self._menus,     0,0)
        self._layout.addWidget(self._statusBar, 1,0,1,2)
    
        self._layout.setRowStretch(0,1)
        self._layout.setRowStretch(1,0)
    
        self._layout.setColumnStretch(0,0)
        self._layout.setColumnStretch(1,1)

        print("open logger for: " + str(probeee))
        if probeee['probeMod'] == 'probe_nchecks':
            cl = probeee['probeClass']
            self._logArea   = NChecksLogArea(self, probe, cl)
            self._layout.addWidget(self._logArea,   0,1)
            print("mod is: " + str(cl))
            
        # old code begin
        else:
            if 'rrd_snmp_table_logger'  in loggers: rrdlogger   = True
            if 'bmonitor_logger_text'   in loggers: textlogger  = True
            if 'bmonitor_logger_event'  in loggers: eventlogger = True

            self._logArea   = LogArea(self, rrdlogger, textlogger, eventlogger, probe)
            self._layout.addWidget(self._logArea,   0,1)
        # old code end
       
        self.show()
 
class NChecksLogArea(AbstractChannelWidget):
    ncheckEvents = pyqtSignal(dict)

    def __init__(self, parent, channel, cl):
        super(NChecksLogArea, self).__init__(parent, channel)
        self.connectProbe()
        layout      = NGridContainer(self)
        rrdGraphDef = nchecks.getGraphTemplateFor(cl)
        for g in rrdGraphDef:
            w = NChecksRrdGraph(g,self)
            self.ncheckEvents.connect(w.handleProbeEvent)
            layout.addWidget(w)
            
    def handleProbeEvent(self, msg): self.ncheckEvents.emit(msg)







class NChecksRrdGraph(NFrameContainer):
    def __init__(self, graphDef, parent=None):
        super(NChecksRrdGraph, self).__init__(parent)
        self._graphDef = graphDef
        self._lab = QLabel(self)
        self._pix = QPixmap()
        self._lab.setText("Generating graphic...")
        tf = NTempFile(self)
        tf.open()
        tf.close()
        self._tf = tf.fileName()
        self._graphDef['filenamePng'] = self._tf
        lay = NGridContainer(self)
        lay.addWidget(self._lab, 0,0)
        lay.setColumnStretch(0,0)
        lay.setColumnStretch(1,1)
        lay.setRowStretch(0,0)
        lay.setRowStretch(1,1)

    def handleProbeEvent(self, msg):
        if msg['type'] == 'nchecksDumpMessage':
            self._graphDef['filenameRrd'] = msg['file']
            self.drawRrd()

    def drawRrd(self):
        pyrrd4j.graph(self._graphDef, self.drawRrdReply)

    def drawRrdReply(self, msg):
        self._pix.load(self._tf)
        self._lab.setPixmap(self._pix)
        
        







# old code
class LogArea(NFrameContainer):
    def __init__(self, parent, rrd, text, event, probe):
        super(LogArea, self).__init__(parent)
        self._layout = NGridContainer(self)

        self._tabs   = QTabWidget(self)
        self._layout.addWidget(self._tabs, 0,0)

        if event == True:
            self._events = QLabel('events', self)
            self._layout.addWidget(self._events, 1,0)
            self._layout.setRowStretch(1,0)
        else:
            self._events = None

        if rrd == True:
            self._rrds = RrdArea(self, probe)
            self._tabs.insertTab(0, self._rrds, QIcon(sysmapi.nGetPixmap('rrdtool-logo')), 'RRD')
        else:
            self._rrds = QLabel('rrds', self)
            self._tabs.insertTab(0, self._rrds, QIcon(sysmapi.nGetPixmap('rrdtool-logo')), 'RRD')
            self._tabs.setTabEnabled(0, False)

        if text == True:
            self._rrds = QLabel('text', self)
            self._tabs.insertTab(1, self._rrds, QIcon(sysmapi.nGetPixmap('accessories-text-editor')), 'Text')
            if self._tabs.isTabEnabled(0) == False:
                self._tabs.setCurrentIndex(1)
        else:
            self._rrds = QLabel('text', self)
            self._tabs.insertTab(1, self._rrds, QIcon(sysmapi.nGetPixmap('accessories-text-editor')), 'Text')
            self._tabs.setTabEnabled(1, False)


class LogStatusBar(QStatusBar):
    def __init__(self, parent):
        super(LogStatusBar, self).__init__(parent)
 

class ProbeMenus(NFrameContainer):
    def __init__(self, parent):
        super(ProbeMenus, self).__init__(parent)
        self._force = QPushButton(self)
        self._force.setIconSize(QSize(30,30))
        self._force.setIcon(QIcon(sysmapi.nGetPixmap('software-update-available')))
        self._pause = QPushButton(self)
        self._pause.setIconSize(QSize(30,30))
        self._pause.setIcon(QIcon(sysmapi.nGetPixmap('media-playback-pause')))
        self._pause.setCheckable(True)
        self._pause.setChecked(False)
        self._action = QPushButton(self)
        self._action.setIconSize(QSize(30,30))
        self._action.setIcon(QIcon(sysmapi.nGetPixmap('utilities-terminal')))
        self._prop = QPushButton(self)
        self._prop.setIconSize(QSize(30,30))
        self._prop.setIcon(QIcon(sysmapi.nGetPixmap('edit-paste')))

        grid = NGridContainer(self)
        grid.setVerticalSpacing(4)
        grid.addWidget(self._force,  0,1)
        grid.addWidget(self._pause,  1,1)
        grid.addWidget(self._action, 2,1)
        grid.addWidget(self._prop,   4,1)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        grid.setRowStretch(2,0)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,0)
        self.setLayout(grid)
