from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    WorkingProbeView    import ProbeView
from    MonitorProxyEvents  import ChannelHandler


class TargetView(QFrame):
    def __init__(self, parent, target, probe):
        super(TargetView, self).__init__(parent)
        self.probeViews = dict()
        self.parent = parent
        self.rowCount   = 1
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.targetHead  = TargetHead(self, target)

        self.targetBody     = QFrame(self)
        self.targetBodyGrid = QGridLayout(self)
        self.targetBody.setLayout(self.targetBodyGrid)

        tab         = QFrame(self)
        tab.setFixedWidth(10)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.targetHead,    0,0,1,2)
        self.grid.addWidget(tab,                1,0)
        self.grid.addWidget(self.targetBody,    1,1)
        self.grid.setColumnStretch(0,0)
        self.grid.setColumnStretch(1,1)
        self.setLayout(self.grid)
        self.newProbe(probe)

    def toggleBody(self):
        if self.grid.itemAtPosition(1,1) == None:
            self.targetBody.show()
            self.grid.addWidget(self.targetBody, 1, 1)
        else:
            self.targetBody.hide()
            self.grid.removeWidget(self.targetBody)

    def newProbe(self, probe):
        self.probeViews[probe] = ProbeView(self, probe)
        self.targetBodyGrid.addWidget(self.probeViews[probe], self.rowCount, 1)
        self.rowCount += 1

    def removeProbe(self, probe):
        self.targetBodyGrid.removeWidget(self.probeViews[probe])
        self.probeViews[probe].deleteLater()
        self.targetBodyGrid.update()
        del self.probeViews[probe]
        if len(self.probeViews) == 0:
            return 'empty'
        else:
            return 'full'

class TargetHead(QFrame):
    def __init__(self, parent, target):
        super(TargetHead, self).__init__(parent)

        self.toggleButton = QPushButton(target, self)
        self.toggleButton.clicked.connect(parent.toggleBody)
        self.toggleButton.setFixedWidth(100)
        self.toggleButton.setFixedHeight(30)

        self.summary    = TargetProbeOverallSummary(self, target)

        self.promoteCheck = QCheckBox('include in Dashboard', self)

        grid = QGridLayout(self)

        #targetLabel = QLabel(target, self)
        grid.addWidget(self.summary,         0, 2, 1, 1)
        grid.addWidget(self.promoteCheck,    0, 4, 1, 1)
        grid.addWidget(self.toggleButton,    0, 0, 1, 1)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,1)
        grid.setColumnStretch(4,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,0)
        self.setLayout(grid)


class TargetProbeOverallSummary(QFrame):
    def __init__(self, parent, target):
        super(TargetProbeOverallSummary, self).__init__(parent)
        self.setFixedWidth(800)
        self.target = target
        sigDict = ChannelHandler.singleton.masterSignalsDict
        sigDict['probeInfo'].signal.connect(self._handleProbeInfo)

        self.buttonDict = dict()
        #self.layout = FlowLayout(self)
        self.layout = QGridLayout(self)
        self.columnCount = 0

        self.setLayout(self.layout)
        self._initializeSummary(target)

    def _initializeSummary(self, target):
        probeDict   = ChannelHandler.singleton.probes
        for probe in probeDict.keys():
            if probeDict[probe]['target'] == target:
                self.buttonDict[probe] = dict()
                self.buttonDict[probe]['column'] = self.columnCount
                status = probeDict[probe]['status']
                self._setButtonStatus(status, probe, self.columnCount)
                self.columnCount += 1
        
    def _setButtonStatus(self, status, probe, column):
        if status == 'OK':
            self.buttonDict[probe]['widget'] = ProbeOkButton(self, probe)
            self.buttonDict[probe]['column'] = column

            self.layout.setColumnStretch(column, 0)
            self.layout.setColumnStretch(column + 1, 1)
            self.layout.addWidget(self.buttonDict[probe]['widget'], 0, column)
        if status == 'CRITICAL':
            self.buttonDict[probe]['widget'] = ProbeCriticalButton(self, probe)
            self.buttonDict[probe]['column'] = column
            
            self.layout.setColumnStretch(column, 0)
            self.layout.setColumnStretch(column + 1, 1)
            self.layout.addWidget(self.buttonDict[probe]['widget'], 0, column)
        if status == 'WARNING':
            self.buttonDict[probe]['widget'] = ProbeWarningButton(self, probe)
            self.buttonDict[probe]['column'] = column
            
            self.layout.setColumnStretch(column, 0)
            self.layout.setColumnStretch(column + 1, 1)
            self.layout.addWidget(self.buttonDict[probe]['widget'], 0, column)

    def _updateButtonStatus(self, status, probe):
        if status == 'OK':
            if 'widget' in self.buttonDict[probe]:
                self.layout.removeWidget(self.buttonDict[probe]['widget'])
                self.buttonDict[probe]['widget'].hide()
                self.buttonDict[probe]['widget'].deleteLater()
                del self.buttonDict[probe]['widget']

            self.buttonDict[probe]['widget'] = ProbeOkButton(self, probe)
            column = self.buttonDict[probe]['column']
            self.layout.addWidget(self.buttonDict[probe]['widget'], 0, column)
        if status == 'CRITICAL':
            if 'widget' in self.buttonDict[probe]:
                self.layout.removeWidget(self.buttonDict[probe]['widget'])
                self.buttonDict[probe]['widget'].hide()
                self.buttonDict[probe]['widget'].deleteLater()
                del self.buttonDict[probe]['widget']

            self.buttonDict[probe]['widget'] = ProbeCriticalButton(self, probe)
            column = self.buttonDict[probe]['column']
            self.layout.addWidget(self.buttonDict[probe]['widget'], 0, column)
        if status == 'WARNING':
            if 'widget' in self.buttonDict[probe]:
                self.layout.removeWidget(self.buttonDict[probe]['widget'])
                self.buttonDict[probe]['widget'].hide()
                self.buttonDict[probe]['widget'].deleteLater()
                del self.buttonDict[probe]['widget']

            self.buttonDict[probe]['widget'] = ProbeWarningButton(self, probe)
            column = self.buttonDict[probe]['column']
            self.layout.addWidget(self.buttonDict[probe]['widget'], 0, column)

    def _handleProbeInfo(self, msg):
        target = msg['value']['target']
        if target == self.target:
            probe  = msg['value']['name']
            status = msg['value']['status']
            self._updateButtonStatus(status, probe)


class ProbeCriticalButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeCriticalButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('\
        QPushButton {   \
            min-height: 1.5em;              \
            font: bold 1em;                       \
            margin: 0 1px 0 1px;            \
            color: white;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #ef2929,    \
                stop: 1 #cc0000);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #a40000;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #ef2929,    \
                stop: 0 #cc0000);           \
        }')

class ProbeWarningButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeWarningButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('QPushButton {   \
            min-height: 1.5em;              \
            font: bold 1em;                       \
            margin: 0 1px 0 1px;            \
            color: white;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #fcaf3e,    \
                stop: 1 #f57900);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #ce5c00;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #fcaf3e,    \
                stop: 0 #f57900);           \
        }')

class ProbeOkButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeOkButton, self).__init__(parent)
        self.setText('   %s   ' % probeName)
        self.setStyleSheet('QPushButton {   \
            min-height: 1.5em;              \
            font: 1em;                       \
            margin: 0 1px 0 1px;            \
            color: white;                   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 0 #a1d99b,    \
                stop: 1 #74c476);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #41ab5d;      \
        }   \
        QPushButton:pressed {   \
            background-color: qlineargradient(  \
                x1: 0,              \
                y1: 0,              \
                x2: 0,              \
                y2: 1,              \
                stop: 1 #a1d99b,    \
                stop: 0 #74c476);           \
        }')
