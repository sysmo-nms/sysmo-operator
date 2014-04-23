from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    PySide.QtSvg        import *
from    PySide.QtWebKit     import *
from    noctopus_widgets    import NFrame
import  nocapi


##################
# SUMMARY WIDGET #
##################
class Summary(NFrame):
    def __init__(self, parent):
        super(Summary, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        self.chanH   = ChannelHandler.singleton
        sigDict     = self.chanH.masterSignalsDict
        sigDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self._initInterface()

    def _initInterface(self):

        grid = QGridLayout(self)

        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(0)

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

class StatusSummary(QPushButton):
    def __init__(self, parent, status):
        super(StatusSummary, self).__init__(parent)
        buttonPol = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(buttonPol)
        self.setFixedHeight(40)
        self.setMinimumWidth(80)

        self.startBlinkTimer()

        # QLCD number
        self.countArea = QLCDNumber(3, self)
        self.countArea.display(888)
        self.countArea.setSegmentStyle(QLCDNumber.Flat)
        self.countArea.setAutoFillBackground(True)
        self.countArea.setBackgroundRole(QPalette.Base)
        self.countArea.setForegroundRole(QPalette.Text)

        self.originalPalette    = self.countArea.palette()
        self.blinkingPalette    = self.countArea.palette()
        self.paletteShift       = 0

        # set blinkingPalette and picutre
        if status == 'OK':
            picture = QSvgWidget(nocapi.nGetImage('weather-clear'), self)
        elif status == 'WARNING':
            picture = QSvgWidget(nocapi.nGetImage('weather-showers'), self)
            self.blinkingPalette.setColor(self.blinkingPalette.Light, QColor(255,255,0))
            self.blinkingPalette.setColor(self.blinkingPalette.Dark, QColor(255,255,0))
        elif status == 'CRITICAL':
            picture = QSvgWidget(nocapi.nGetImage('weather-severe-alert'), self)
            self.blinkingPalette.setColor(self.blinkingPalette.Light, QColor(255,0,0))
            self.blinkingPalette.setColor(self.blinkingPalette.Dark, QColor(255,0,0))
        elif status == 'UNKNOWN':
            picture = QSvgWidget(nocapi.nGetImage('weather-clear-night'), self)

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



##############
# OSM WIDGET #
##############
class OSMView(QFrame):
    def __init__(self, parent):
        super(OSMView, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

        self.osm    = QWebView(self)
        # XXX Found bug here. QWebView do not properly quit on application
        # shutdow when he is loading a page.
        #self.osm.load(QUrl('./html/OpenStreetMap.html'))

        self.shade = QFrame(self)
        self.shade.setAutoFillBackground(False)
        self.shade.hide()
        self._browsable = True

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.osm, 0,0)
        self.setLayout(self.grid)

    def setBrowsable(self, bol):
        if  bol == False and self._browsable == True:
            self.shade.show()
            self.grid.addWidget(self.shade, 0,0)
            self.shadeStatus = False
        elif bol == True and self._browsable == False:
            self.shade.hide()
            self.grid.removeWidget(self.shade)
            self.shadeStatus = True


##################
# CUSTOM BUTTONS #
##################
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
            color: black;                   \
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

class ProbeUnknownButton(QPushButton):
    def __init__(self, parent, probeName):
        super(ProbeUnknownButton, self).__init__(parent)
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
                stop: 0 #666666,    \
                stop: 1 #222222);           \
            border-style: outset;       \
            border-radius: 3px;         \
            border-width: 1px;          \
            border-color: #aaaaaa;      \
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
