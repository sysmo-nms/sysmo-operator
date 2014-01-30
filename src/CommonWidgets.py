from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    MonitorProxyEvents  import *
import  TkorderIcons


class Summary(QFrame):
    def __init__(self, parent):
        super(Summary, self).__init__(parent)
        self.chanH   = ChannelHandler.singleton
        sigDict     = self.chanH.masterSignalsDict
        sigDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self._initInterface()

    def _initInterface(self):

        grid = QGridLayout(self)

        self.okWidget       = StatusSummary(self, 'OK')
        self.warningWidget  = StatusSummary(self, 'WARNING')
        self.criticalWidget = StatusSummary(self, 'CRITICAL')
        self.unknownWidget  = StatusSummary(self, 'UNKNOWN')


        grid.addWidget(self.okWidget,       0,0)
        grid.addWidget(self.warningWidget,  0,1)
        grid.addWidget(self.criticalWidget, 0,2)
        grid.addWidget(self.unknownWidget,  0,3)
        
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,0)
        grid.setColumnStretch(4,1)
        self.setLayout(grid)
        self._setCounters()

    def _setCounters(self):
        probes      = self.chanH.probes
        ok          = 0
        warning     = 0
        critical    = 0
        unknown     = 0
        
        for key in probes:
            status = probes[key]['status']
            if      status == 'OK':         ok       += 1
            elif    status == 'WARNING':    warning  += 1
            elif    status == 'CRITICAL':   critical += 1
            elif    status == 'UNKNOWN':    unknown  += 1

        self.okWidget.setCount(ok)
        self.warningWidget.setCount(warning)
        self.criticalWidget.setCount(critical)
        self.unknownWidget.setCount(unknown)

        if critical != 0:   self.criticalWidget.setBlink(True)
        else:               self.criticalWidget.setBlink(False)
        if warning  != 0:   self.warningWidget.setBlink(True)
        else:               self.warningWidget.setBlink(False)

        
    def _handleProbeInfo(self, msg): 
        self._setCounters()

class StatusSummary(QFrame):
    def __init__(self, parent, status):
        super(StatusSummary, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.startBlinkTimer()

        # QLCD number
        self.countArea = QLCDNumber(2, self)
        self.countArea.display(99)
        self.countArea.setSegmentStyle(QLCDNumber.Flat)
        self.countArea.setAutoFillBackground(True)
        self.countArea.setBackgroundRole(QPalette.Base)
        self.countArea.setForegroundRole(QPalette.Text)

        self.originalPalette    = self.countArea.palette()
        self.blinkingPalette    = self.countArea.palette()
        self.paletteShift       = 0

        # set blinkingPalette and picutre
        if status == 'OK':
            picture = QSvgWidget(TkorderIcons.getImage('weather-clear'), self)
        elif status == 'WARNING':
            picture = QSvgWidget(TkorderIcons.getImage('weather-showers'), self)
            self.blinkingPalette.setColor(self.blinkingPalette.Light, QColor(255,255,0))
            self.blinkingPalette.setColor(self.blinkingPalette.Dark, QColor(255,255,0))
        elif status == 'CRITICAL':
            picture = QSvgWidget(TkorderIcons.getImage('weather-severe-alert'), self)
            self.blinkingPalette.setColor(self.blinkingPalette.Light, QColor(255,0,0))
            self.blinkingPalette.setColor(self.blinkingPalette.Dark, QColor(255,0,0))
        elif status == 'UNKNOWN':
            picture = QSvgWidget(TkorderIcons.getImage('weather-clear-night'), self)

        picture.setFixedHeight(30)
        picture.setFixedWidth(30)


        grid = QGridLayout(self)
        grid.addWidget(picture,         0,0)
        grid.addWidget(self.countArea,   0,1)
        self.setLayout(grid)

    def setCount(self, value):
        self.countArea.display(value)

    def setBlink(self, bol):
        if  bol == True:
            self.blinking = True
        else:
            self.blinking = False
            self.countArea.setPalette(self.originalPalette)

    def startBlinkTimer(self):
        self.blinking   = False
        self.asyncBlink = 2
        self.blinkTimer = QTimer(self)
        self.blinkTimer.timeout.connect(self.blink)
        self.blinkTimer.start(500)

    def blink(self):
        if self.blinking == True:
            if self.paletteShift == 0:
                self.countArea.setPalette(self.blinkingPalette)
                if self.asyncBlink == 0:
                    self.paletteShift = 1
                    self.asyncBlink = 2
                else:
                    self.asyncBlink -= 1
            elif self.paletteShift == 1:
                self.countArea.setPalette(self.originalPalette)
                self.paletteShift = 0
