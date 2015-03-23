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

from    monitor.proxy import AbstractChannelWidget, ChanHandler
from    monitor.dialogs.properties.probe.rrdarea  import RrdArea
import  monitor.api    as monapi
import  monitor.norrd  as norrd

import  sysmapi
import  platform
import  re

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
        
        print("open logger for: " + str(probeee))
        if probeee['probeMod'] == 'probe_nchecks':
            cl = probeee['probeClass']
            print("mod is: " + str(cl))
            pass
            
        else:
            if 'rrd_snmp_table_logger'  in loggers: rrdlogger   = True
            if 'bmonitor_logger_text'   in loggers: textlogger  = True
            if 'bmonitor_logger_event'  in loggers: eventlogger = True

            self._logArea   = LogArea(self, rrdlogger, textlogger, eventlogger, probe)

            self._layout    = NGrid(self)
            self._layout.addWidget(self._menus,     0,0)
            self._layout.addWidget(self._logArea,   0,1)
            self._layout.addWidget(self._statusBar, 1,0,1,2)
    
            self._layout.setRowStretch(0,1)
            self._layout.setRowStretch(1,0)
    
            self._layout.setColumnStretch(0,0)
            self._layout.setColumnStretch(1,1)

        self.show()
 
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
