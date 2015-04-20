from    PyQt5.QtCore   import (
    QSettings,
    QSize,
    QTimeLine,
    pyqtSignal,
    Qt,
    QTimer
)

from    PyQt5.QtGui    import (
    QPixmap,
    QIcon,
    QPalette,
    QFont
)

from    PyQt5.QtWidgets    import (
    QLabel,
    QWidget,
    QDialog,
    QAbstractScrollArea,
    QStatusBar,
    QProgressBar,
    QPushButton,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QTabWidget,
    QFrame,
    QLayout,
    QScrollArea,
    QMdiSubWindow
)

from    sysmo_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid
)

from    monitor.proxy import AbstractChannelWidget, ChanHandler, NTempFile
import  monitor.api    as monapi

import  sysmapi
import  pyrrd4j
import  platform
import  nchecks
import  re
import  os
import  sys


def openPerformancesMDIFor(probe):
    if probe in list(LoggerMDI.Elements.keys()):
        LoggerMDI.Elements[probe].show()
    else:
        LoggerMDI.Elements[probe] = LoggerMDI(probe) 

class LoggerMDI(QMdiSubWindow):
    Elements = dict()
    def __init__(self, probe, displayName="undefined", parent=None):
        super(LoggerMDI, self).__init__(parent)
        sysmapi.nConnectWillClose(self.close)
        self.setWidget(LoggerContainer(probe,displayName,self))
    


def openPerformancesFor(probe, displayName):
    if probe in list(LoggerView.Elements.keys()):
        LoggerView.Elements[probe].show()
    else:
        LoggerView.Elements[probe] = LoggerView(probe, displayName)

class LoggerView(QDialog):
    Elements = dict()
    def __init__(self, probe, displayName, parent=None):
        super(LoggerView, self).__init__(parent)
        sysmapi.nConnectWillClose(self.close)
        lay = NGridContainer(self)
        lay.addWidget(LoggerContainer(probe, displayName, self))
        self.show()

class LoggerContainer(NFrameContainer):
    def __init__(self, probe, displayName, parent=None):
        super(LoggerContainer, self).__init__(parent)

        self._statusBar = LogStatusBar(self)
        self._menus     = ProbeMenus(self)

        probeDict = ChanHandler.singleton.probes[probe]

        self._layout    = NGrid(self)
        self._layout.addWidget(self._menus,     0,0)
        self._layout.addWidget(self._statusBar, 1,0,1,2)
    
        self._layout.setRowStretch(0,1)
        self._layout.setRowStretch(1,0)
    
        self._layout.setColumnStretch(0,0)
        self._layout.setColumnStretch(1,1)

        nchecksClass = probeDict['probeClass']
        self._logArea = NChecksLogArea(self, probe, nchecksClass)
        self._layout.addWidget(self._logArea,   0,1)

class NChecksLogArea(AbstractChannelWidget):
    ncheckEvents = pyqtSignal(dict)
    widthEvents  = pyqtSignal(int)

    def __init__(self, parent, channel, cl):
        super(NChecksLogArea, self).__init__(parent, channel)
        self._widthTimer = QTimer(self)
        self._widthTimer.setSingleShot(True)
        self._widthTimer.setInterval(500)
        self._widthTimer.timeout.connect(self._widthSignal)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Light)
        self.setFrameShape(QFrame.StyledPanel)
        #self.setFrameShadow(QFrame.Raised)

        layout      = NGrid(self)
        layout.setContentsMargins(7,5,5,5)

        graphFrame = NFrame(self)
        graphFrame.setAutoFillBackground(True)
        graphFrame.setBackgroundRole(QPalette.Window)
        graphFrame.setFrameShape(QFrame.Panel)
        graphFrame.setFrameShadow(QFrame.Sunken)
        graphGrid = NGrid(graphFrame)
        
        scroll = QScrollArea(self)
        scroll.setMinimumWidth(400)
        scroll.setMinimumHeight(200)
        scroll.setWidget(graphFrame)
        scroll.setWidgetResizable(True)
        self._controls = NChecksRrdControls(self)
        layout.addWidget(self._controls,    0,0)
        layout.addWidget(scroll,        1,0)
        layout.setRowStretch(0,0)
        layout.setRowStretch(1,1)


        (gtype, rrdGraphDef) = nchecks.getGraphTemplateFor(cl)
        if gtype == "simple":
            row = 0
            for g in rrdGraphDef:
                w = NChecksRrdGraph(g,self)
                self.ncheckEvents.connect(w.handleProbeEvent)
                self.widthEvents.connect(w.widthChanged)
                self._controls.heightCtrl.currentIndexChanged[int].connect(w.heightChanged)
                self._controls.timeLineCtrl.currentIndexChanged[int].connect(w.timeChanged)
                graphGrid.addWidget(w, row, 0)
                graphGrid.setRowStretch(row, 0)
                row += 1
            graphGrid.setRowStretch(row, 1)
        elif gtype == "table":
            propertyInfo = nchecks.getTableIndexInfoFor(cl)
            w = NChecksRrdGraphTable(rrdGraphDef, propertyInfo, channel, self)
            self.ncheckEvents.connect(w.handleProbeEvent)
            self.widthEvents.connect(w.widthChanged)
            self._controls.heightCtrl.currentIndexChanged[int].connect(w.heightChanged)
            self._controls.timeLineCtrl.currentIndexChanged[int].connect(w.timeChanged)
            graphGrid.addWidget(w)
        self.connectProbe()

    def handleProbeEvent(self, msg):
        self.ncheckEvents.emit(msg)

    def widthEvent(self, width):
        self.widthEvents.emit(width)

    def resizeEvent(self, event):
        self._widthTimer.start()
    
    def _widthSignal(self):
        self.widthEvents.emit(self.size().width())

def pr(val):
    print(val)
    sys.stdout.flush()


class NChecksRrdGraphTable(NFrameContainer):
    
    nchecksEvents   = pyqtSignal(dict)
    widthEvents     = pyqtSignal(int)
    timeEvents      = pyqtSignal(int)
    heightEvents    = pyqtSignal(int)

    def __init__(self, graphDefs, propertyInfo, channel, parent=None):
        super(NChecksRrdGraphTable, self).__init__(parent)
        self._graphDefinitions = graphDefs
        targetName = monapi.getProbesDict()[channel]['target']
        target = monapi.getTarget(targetName)
        self._properties = target['properties']
        self._propertyInfo = propertyInfo
        

 
    def handleProbeEvent(self, msg):
        if msg['type'] == 'nchecksTableDumpMessage':
            elementToFile = msg['elementToFile']
            grid = NGridContainer(self)
            rowid = 0
            for idx in elementToFile.keys():
                row = NChecksRrdGraphRow(
                    self._graphDefinitions, idx, self._propertyInfo, self._properties, self)
                self.widthEvents[int].connect(row.widthChanged)
                grid.addWidget(row, rowid, 0)
                grid.setRowStretch(rowid, 0)
                rowid += 1
            grid.setRowStretch(rowid, 1)

        self.nchecksEvents.emit(msg)
            
    def widthChanged(self, size): self.widthEvents.emit(size)

    def heightChanged(self, size): self.heightEvents.emit(size)

    def timeChanged(self, seconds): self.timeEvents.emit(seconds)


class NChecksRrdGraphRow(NFrameContainer):

    widthEvents  = pyqtSignal(int)

    def __init__(self, graphDefs, idx, propInfo, properties, parent=None):
        super(NChecksRrdGraphRow, self).__init__(parent)
        self._idx = idx
        self._rowNumber = len(graphDefs)
        grid = NGridContainer(self)
        
        (prefix, suffix) = propInfo
        targetProperty = prefix + idx + suffix
        if targetProperty in properties.keys():
            text = "<h3>%s</h3>" % properties[targetProperty]
        else:
            text = "<h3>(%s)</h3>" % targetProperty
        lab = QLabel(text, self)
        lab.setFixedWidth(50)
        grid.addWidget(lab, 0, 0)

        colid = 1
        for gdef in graphDefs:
            graph = NChecksRrdGraph(gdef, self)
            graph.setIdx(idx)
            parent.heightEvents[int].connect(graph.heightChanged)
            parent.timeEvents[int].connect(graph.timeChanged)
            parent.nchecksEvents[dict].connect(graph.handleProbeEvent)
            self.widthEvents[int].connect(graph.widthChanged)
 
            grid.addWidget(graph, 0, colid)
            colid += 1

    def widthChanged(self, size):
        self.widthEvents.emit(size / self._rowNumber)

class NChecksRrdGraph(NFrameContainer):
    def __init__(self, gdef, parent=None):
        super(NChecksRrdGraph, self).__init__(parent)
        self._gdef = gdef.copy()
        self._setGraphHeight(NChecksRrdControls.SIZE_NORMAL)
        self._setGraphTime(NChecksRrdControls.TIME_SEVEN_DAYS)
        self._lab = QLabel(self)
        self._pix = QPixmap()
        self._lab.setText("Generating graphic...")
        tfile = NTempFile(self)
        tfile.open()
        tfile.close()
        self._filename = tfile.fileName()
        self._gdef['filenamePng'] = self._filename
        lay = NGridContainer(self)
        lay.addWidget(self._lab, 0,0)
        lay.setColumnStretch(0,0)
        lay.setColumnStretch(1,1)
        lay.setRowStretch(0,0)
        lay.setRowStretch(1,1)

    # for table type only
    def setIdx(self, idx): self._idx = idx

    def widthChanged(self, size):
        self._setGraphWidth(size - 150)
        self._drawRrd()
        
    def heightChanged(self, size):
        self._setGraphHeight(size)
        self._drawRrd()

    def timeChanged(self, time):
        self._setGraphTime(time)
        self._drawRrd()

    def handleProbeEvent(self, msg):
        if msg['type'] == 'nchecksSimpleDumpMessage':
            self._gdef['filenameRrd'] = msg['file']
            self._drawRrd()
        elif msg['type'] == 'nchecksSimpleUpdateMessage' and self._gdef['filenameRrd'] != None:
            self._drawRrd()
        elif msg['type'] == 'nchecksTableDumpMessage':
            self._gdef['filenameRrd'] = msg['elementToFile'][self._idx]
            self._drawRrd()
        elif msg['type'] == 'nchecksTableUpdateMessage' and self._gdef['filenameRrd'] != None:
            self._drawRrd()

    def _drawRrd(self):
        if self._gdef['filenameRrd'] == None: return
        pyrrd4j.graph(self._gdef, self._drawRrdReply)

    def _drawRrdReply(self, msg):
        self._pix.load(self._filename)
        self._lab.setPixmap(self._pix)
        if msg == "OK": return
        print("draw error: " + msg)

    def _setGraphWidth(self, size):
        self._gdef['width'] = size

    def _setGraphHeight(self, size):
        if size == NChecksRrdControls.SIZE_THUMBNAIL:
            self._gdef['height'] = 30
        elif size == NChecksRrdControls.SIZE_SMALL:
            self._gdef['height'] = 50
        elif size == NChecksRrdControls.SIZE_NORMAL:
            self._gdef['height'] = 100 
        elif size == NChecksRrdControls.SIZE_LARGE:
            self._gdef['height'] = 180
        elif size == NChecksRrdControls.SIZE_HUGE:
            self._gdef['height'] = 300
    
    def _setGraphTime(self, time):
        if time == NChecksRrdControls.TIME_TWO_HOURS:
            self._gdef['spanBegin'] = -7200
        elif time == NChecksRrdControls.TIME_TWELVE_HOURS:
            self._gdef['spanBegin'] = -43200
        elif time == NChecksRrdControls.TIME_TWO_DAYS:
            self._gdef['spanBegin'] = -172800
        elif time == NChecksRrdControls.TIME_SEVEN_DAYS:
            self._gdef['spanBegin'] = -604800
        elif time == NChecksRrdControls.TIME_TWO_WEEKS:
            self._gdef['spanBegin'] = -1209600
        elif time == NChecksRrdControls.TIME_ONE_MONTH:
            self._gdef['spanBegin'] = -2592000
        elif time == NChecksRrdControls.TIME_SIX_MONTHS:
            self._gdef['spanBegin'] = -15552000
        elif time == NChecksRrdControls.TIME_ONE_YEAR:
            self._gdef['spanBegin'] = -31536000
        elif time == NChecksRrdControls.TIME_THREE_YEARS:
            self._gdef['spanBegin'] = -94608000
        elif time == NChecksRrdControls.TIME_TEN_YEARS:
            self._gdef['spanBegin'] = -315360000
        

class NChecksRrdControls(NFrameContainer):
    TIME_TWO_HOURS      = 0
    TIME_TWELVE_HOURS   = 1
    TIME_TWO_DAYS       = 2
    TIME_SEVEN_DAYS     = 3
    TIME_TWO_WEEKS      = 4
    TIME_ONE_MONTH      = 5
    TIME_SIX_MONTHS     = 6
    TIME_ONE_YEAR       = 7
    TIME_THREE_YEARS    = 8
    TIME_TEN_YEARS      = 9
    
    SIZE_THUMBNAIL  = 0
    SIZE_SMALL      = 1
    SIZE_NORMAL     = 2
    SIZE_LARGE      = 3
    SIZE_HUGE       = 4

    def __init__(self, parent):
        super(NChecksRrdControls, self).__init__(parent)
        self._layout = NGridContainer(self)

        self._timeLineLabel = QLabel('Timeline:', self)
        self.timeLineCtrl = QComboBox(self)
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_TWO_HOURS,     '2h  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_TWELVE_HOURS,  '12h from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_TWO_DAYS,      '2d  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_SEVEN_DAYS,    '7d  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_TWO_WEEKS,     '2w  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_ONE_MONTH,     '1m  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_SIX_MONTHS,    '6m  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_ONE_YEAR,      '1y  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_THREE_YEARS,   '3y  from now')
        self.timeLineCtrl.insertItem(NChecksRrdControls.TIME_TEN_YEARS,     '10y from now')
        self.timeLineCtrl.setCurrentIndex(NChecksRrdControls.TIME_SEVEN_DAYS)

        self._layout.addWidget(self._timeLineLabel, 0,0)
        self._layout.addWidget(self.timeLineCtrl,   0,1)

        self._heightLabel = QLabel('Graph height:', self)
        self.heightCtrl = QComboBox(self)
        self.heightCtrl.insertItem(NChecksRrdControls.SIZE_THUMBNAIL,   'Thumbnail')
        self.heightCtrl.insertItem(NChecksRrdControls.SIZE_SMALL,       'Small')
        self.heightCtrl.insertItem(NChecksRrdControls.SIZE_NORMAL,      'Normal')
        self.heightCtrl.insertItem(NChecksRrdControls.SIZE_LARGE,       'Large')
        self.heightCtrl.insertItem(NChecksRrdControls.SIZE_HUGE,        'Huge')
        self.heightCtrl.setCurrentIndex(NChecksRrdControls.SIZE_NORMAL)
        self._layout.addWidget(self._heightLabel, 0,2)
        self._layout.addWidget(self.heightCtrl,   0,3)

        self._layout.setColumnStretch(0,0)
        self._layout.setColumnStretch(1,0)
        self._layout.setColumnStretch(2,0)
        self._layout.setColumnStretch(3,0)
        self._layout.setColumnStretch(4,1)


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
