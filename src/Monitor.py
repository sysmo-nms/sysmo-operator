from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  os
import  re
import  norrdQtThreaded

from    MonitorProxyEvents  import ChannelHandler
from    CommonWidgets       import *
import  MonitorDashboardArea
import  MonitorTreeArea
import  TkorderMain

class MonitorMain(QSplitter):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(MonitorMain, self).__init__(parent)
        norrdQtThreaded.init(parent=self)

        self.setObjectName('monitorMain splitter')
        tko = TkorderMain.TkorderClient.singleton
        tko.closeSignal.connect(self.saveLayoutState)
        MonitorMain.singleton   = self
        self.eventHandler       = ChannelHandler(self, 5)

        self.collapsed  = False

        self.leftTree   = MonitorTreeArea.TreeContainer(self)
        self.rightDash  = MonitorDashboardArea.DashboardStack(self)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightDash)
        
        tko.addTopDockWidget(Summary(self), 'Monitoriii')

        self.targets    = dict()
        self.initHexaPalettes()
        #self.readLayoutState()

    def toggleButtonClicked(self):
        if self.collapsed == False:
            self.leftTree.hide()
            self.collapsed = True
        elif self.collapsed == True:
            self.leftTree.show()
            self.collapsed = False

    def setMinimalView(self, bol):
        if bol == True:
            self.rightDash.hide()
            MonitorTreeArea.TreeContainer.singleton.setMinimalView(True)
        else:
            self.rightDash.show()
            MonitorTreeArea.TreeContainer.singleton.setMinimalView(False)


    def handleMsg(self, msg):
        mType = msg['msgType']

        if   (mType == 'probeInfo'):      self.signals.probeInfo.emit(msg)
        elif (mType == 'probeModInfo'):   self.signals.probeModInfo.emit(msg)
        elif (mType == 'targetInfo'):     self.signals.targetInfo.emit(msg)
        elif (mType == 'probeActivity'):  self.signals.probeActivity.emit(msg)
        elif (mType == 'subscribeOk'):    self.signals.subscribeOk.emit(msg)
        elif (mType == 'probeDump'):      self.signals.probeDump.emit(msg)
        elif (mType == 'probeReturn'):    self.signals.probeReturn.emit(msg)
        elif (mType == 'unsubscribeOk'):  self.signals.unsubscribeOk.emit(msg)
        else:   print "unknown message type: ", mType

    def initHexaPalettes(self):

        " For widgets who need hexadecimal version of the colors actualy used "
        " by the application (rrdtool)"

        self.rgbDict    = dict()
        self.rgbaDict   = dict()
        pal             = self.palette()
        constDict = {
            'Window':       QPalette.Window,
            'WindowText':   QPalette.WindowText,
            'Base':         QPalette.Base,
            'AlternateBase':    QPalette.AlternateBase,
            'ToolTipBase':  QPalette.ToolTipBase,
            'ToolTipText':  QPalette.ToolTipText,
            'Text':         QPalette.Text,
            'Button':       QPalette.Button,
            'ButtonText':   QPalette.ButtonText,
            'BrightText':   QPalette.BrightText,
            'Light':        QPalette.Light,
            'MidLight':     QPalette.Midlight,
            'Dark':         QPalette.Dark,
            'Mid':          QPalette.Mid,
            'Shadow':       QPalette.Shadow
        }

        for key in constDict.keys():
            col         = pal.color(constDict[key])
            (r,g,b,a)   = col.getRgb()
            self.rgbaDict[key]  = "#%0.2X%0.2X%0.2X%0.2X" % (r,g,b,a)
            self.rgbDict[key] = "#%0.2X%0.2X%0.2X" % (r,g,b)
    
    def readLayoutState(self):
        settings = QSettings("Kmars", "monitor")
        self.restoreGeometry(settings.value("Monitor/geometry"))
        self.restoreState(settings.value("Monitor/state"))

    def saveLayoutState(self):
        settings = QSettings("Kmars", "monitor")
        settings.setValue("Monitor/geometry",   self.saveGeometry())
        settings.setValue("Monitor/state",      self.saveState())
