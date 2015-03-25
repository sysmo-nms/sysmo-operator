from    PyQt5.QtCore   import (
    QObject,
    QTemporaryFile,
    QSettings,
    QSize,
    QTimeLine,
    pyqtSignal,
    Qt
)

from    PyQt5.QtGui    import (
    QPalette,
    QFont,
    QPixmap
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

from    monitor.proxy  import AbstractChannelWidget, ChanHandler
import  monitor.api    as monapi
import  monitor.norrd  as norrd
from    sysmo_widgets import NTemporaryFile

import  sysmapi
import  platform
import  tempfile
import  re
import  os

class RrdArea(NFrameContainer):
    def __init__(self, parent, probe):
        super(RrdArea, self).__init__(parent)
        self._rrdFrame = RrdFrame(self, probe)
        self._rrdScroll = QScrollArea(self)
        self._rrdScroll.setMinimumWidth(400)
        self._rrdScroll.setMinimumHeight(200)
        self._rrdScroll.setWidget(self._rrdFrame)
        self._rrdScroll.setWidgetResizable(True)

        rrdControls = RrdControls(self)
        grid = NGrid(self)
        grid.setVerticalSpacing(4)
        grid.addWidget(rrdControls,     0,0)
        grid.addWidget(self._rrdScroll, 0,1)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        self.setLayout(grid)

class RrdFrame(AbstractChannelWidget):
    def __init__(self, parent, probe):
        super(RrdFrame, self).__init__(parent, probe)

        self._layout = NGrid(self)
        self._graphElements = dict()
        self._probeName = probe
        self._probeConf = monapi.getProbesDict()[probe]
        rrdConf = self._probeConf['loggers']['rrd_snmp_table_logger']
        for i in range(len(rrdConf['indexes'])):
            index = rrdConf['indexes'][i]
            self._graphElements[index] = RrdGraphArea(self, index, rrdConf['rgraphs'])
            self._layout.addWidget(self._graphElements[index], i, 0)
            self._layout.setRowStretch(i, 0)

        self._layout.setRowStretch(len(rrdConf['indexes']), 1)
        self.connectProbe()

    def handleProbeEvent(self, msg):
        if msg['type'] == 'loggerRrdEvent':
            index = msg['data']
            self._graphElements[int(index)].rrdUpdateEvent()
        elif msg['type'] == 'probeDump':
            if msg['logger'] == 'rrd_snmp_table_logger':
                (index, rrdDbFile) = msg['data']
                self._graphElements[int(index)].setRrdDbFile(rrdDbFile)

class RrdGraphArea(NFrameContainer):
    def __init__(self, parent, index, graphConf):
        super(RrdGraphArea, self).__init__(parent)
        self._layout    = NGridContainer(self)
        self._graphs    = dict()
        self._index     = index
        self._graphConf = graphConf
        print("graph is:" , graphConf)
        for gindex, _ in enumerate(graphConf):
            self._graphs[gindex] = RrdGraph(self, graphConf[gindex])
            self._layout.addWidget(self._graphs[gindex], 0,gindex)

    def setRrdDbFile(self, fileName):
        for key in list(self._graphs.keys()):
            self._graphs[key].setRrdDbFile(fileName)
        self.rrdUpdateEvent()

    def rrdUpdateEvent(self):
        for key in list(self._graphs.keys()):
            self._graphs[key].rrdUpdateEvent()


class RrdGraph(QLabel):
    def __init__(self, parent, graphConf):
        super(RrdGraph, self).__init__(parent)
        self._rrdGraphFile      = NTemporaryFile(self)
        self._rrdGraphFileName  = self._rrdGraphFile.fileName()
        self._rrdPixmap         = QPixmap()
        self.setPixmap(self._rrdPixmap)
        #if platform.system() == 'Windows':
            #winfileName = os.path.normpath(self._rrdGraphFileName)
            #print("old filename: ", self._rrdGraphFileName, " new file name: ", winfileName)
            #self._rrdGraphFile = winfileName
        #else:
            #self._rrdGraphFile = filename

        self._rrdDbFileName = None
        self._rrdGraphOpts  = None
        self._rrdGraph      = graphConf

    def setRrdDbFile(self, fileName):
        if platform.system() == 'Windows':
            winfileName = os.path.normpath(fileName)
            self._rrdDbFileName = winfileName

            rrdWinfile0  = winfileName.replace("\\", "\\\\")
            rrdWinfile1  = rrdWinfile0.replace(":","\\:")
            self._rrdGraph = re.sub('<FILE>', rrdWinfile1, self._rrdGraph)

        else:
            self._rrdDbFileName = fileName
            self._rrdGraph = re.sub('<FILE>', fileName, self._rrdGraph)

#--border 0 \
        self._rrdGraphOpts = '\
--full-size-mode \
--disable-rrdtool-tag \
--slope-mode \
--tabwidth 1 \
--color BACK#00000000 \
--color CANVAS%s \
--color GRID%s \
--color MGRID%s \
--color FONT%s \
--color AXIS%s \
--color FRAME%s \
--color SHADEA%s \
--color SHADEB%s \
--color ARROW%s ' % (
                sysmapi.nGetRgba('Base'),
                sysmapi.nGetRgba('Dark'),
                sysmapi.nGetRgba('Shadow'),
                sysmapi.nGetRgba('WindowText'),
                sysmapi.nGetRgba('Dark'),
                sysmapi.nGetRgba('Window'),
                sysmapi.nGetRgba('Window'),
                sysmapi.nGetRgba('Window'),
                sysmapi.nGetRgba('Shadow')
            )

    def rrdUpdateEvent(self):
        cmd = self._generateGraphCmd()
        norrd.cmd(
            cmd,
            callback=self._rrdUpdateReply,
            data=self._rrdGraphFileName)

    def _rrdUpdateReply(self, rrdreply):
        self._rrdPixmap.load(self._rrdGraphFileName)
        self.setPixmap(self._rrdPixmap)

    def _generateGraphCmd(self):
        return "graph %s %s %s" % (
            self._rrdGraphFileName,
            self._rrdGraphOpts,
            self._rrdGraph)

class RrdControls(NFrameContainer):
    def __init__(self, parent):
        super(RrdControls, self).__init__(parent)
        self._layout = NGridContainer(self)
        self._layout.setRowStretch(10, 1)

        self._locateLabel   = QLabel('Search:', self)
        self._locateCtrl    = QLineEdit(self)
        self._layout.addWidget(self._locateLabel, 0,0)
        self._layout.addWidget(self._locateCtrl,  0,1)
        self._layout.setRowStretch(0,0)

        self._timeLineLabel = QLabel('Timeline:', self)
        self._timeLineCtrl = QComboBox(self)
        self._timeLineCtrl.insertItem(0, '2h  from now')
        self._timeLineCtrl.insertItem(1, '12h from now')
        self._timeLineCtrl.insertItem(2, '2d  from now')
        self._timeLineCtrl.insertItem(3, '7d  from now')
        self._timeLineCtrl.insertItem(4, '2w  from now')
        self._timeLineCtrl.insertItem(5, '1m  from now')
        self._timeLineCtrl.insertItem(6, '6m  from now')
        self._timeLineCtrl.insertItem(7, '1y  from now')
        self._timeLineCtrl.insertItem(8, '3y  from now')
        self._timeLineCtrl.insertItem(9, '10y from now')
        self._layout.addWidget(self._timeLineLabel, 1,0)
        self._layout.addWidget(self._timeLineCtrl,  1,1)
        self._layout.setRowStretch(1,0)

        self._heightLabel = QLabel('Graph height:', self)
        self._heightCtrl = QComboBox(self)
        self._heightCtrl.insertItem(0, 'Thumbnail')
        self._heightCtrl.insertItem(1, 'Small')
        self._heightCtrl.insertItem(2, 'Normal')
        self._heightCtrl.insertItem(3, 'Large')
        self._heightCtrl.insertItem(4, 'Huge')
        self._layout.addWidget(self._heightLabel, 2,0)
        self._layout.addWidget(self._heightCtrl,  2,1)
        self._layout.setRowStretch(2,0)
 
        self._layoutLabel = QLabel('Layout:', self)
        self._layoutCtrl = QComboBox(self)
        self._layoutCtrl.addItem('1 column')
        self._layoutCtrl.addItem('2 columns')
        self._layoutCtrl.addItem('3 columns')
        self._layoutCtrl.addItem('4 columns')
        self._layout.addWidget(self._layoutLabel, 3,0)
        self._layout.addWidget(self._layoutCtrl,  3,1)
        self._layout.setRowStretch(3,0)
 
        self._unifyLabel = QLabel('Unify Y axis:', self)
        self._unifyCtrl  = QCheckBox(self)
        self._layout.addWidget(self._unifyLabel, 4,0)
        self._layout.addWidget(self._unifyCtrl,  4,1)
        self._layout.setRowStretch(4,0)
