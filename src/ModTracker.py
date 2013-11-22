from    PySide.QtGui    import *
from    PySide.QtCore   import *
import  TkorderIcons
import  Supercast
import  os
import  re

from    ModTrackerEvents import TrackerEvents
import  ModTrackerWideView
import  ModTrackerTarget
import  ModTrackerTreeArea

class TrackerMain(QSplitter):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(TrackerMain, self).__init__(parent)

        TrackerMain.singleton = self
        self.signals    = TrackerEvents(self)
        self.vardir     = os.path.join(os.getcwd(), 'var')

        " forward 'modTrackerPDU to me "
        Supercast.Link.setMessageProcessor('modTrackerPDU', self.handleMsg)

        self.leftTree   = ModTrackerTreeArea.TreeContainer(self)
        self.rightStack = ModTrackerTarget.Stack(self)

        self.addWidget(self.leftTree)
        self.addWidget(self.rightStack)
        
        TrackerEvents.singleton.probeInfo.connect(self.handleProbeInfo)
        TrackerEvents.singleton.probeModInfo.connect(self.handleProbeModInfo)
        
        self.targets    = dict()
        self.initHexaPalettes()
        self.initView()

    def initView(self):
        self.rightStack.addWidget(ModTrackerWideView.View(self))

    def handleProbeModInfo(self, msg): pass

    def handleProbeInfo(self, msg):
        # TODO integrade the targets dict() with ModTrackerTreeArea
        probeInfo   = msg['value']
        channel     = probeInfo['channel']
        probeId     = probeInfo['id']
        if channel in self.targets:
            self.targets[channel][probeId]  = probeInfo
        else:
            self.targets[channel]           = dict()
            self.targets[channel][probeId]  = probeInfo

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
        " by the application "

        self.colorDict = dict()
        pal     = self.palette()
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
            self.colorDict[key] = "#%0.2X%0.2X%0.2X%0.2X" % (r,g,b,a)
