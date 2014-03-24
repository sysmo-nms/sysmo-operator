
# python libs

import  os
import  re

# Qt
from    PySide.QtGui    import *
from    PySide.QtCore   import *

# local libs
#from    Monitor.widgetsCommon   import Summary

from  Monitor           import norrd
#import  MonitorDashboardArea
#import  MonitorTreeArea
import  noctopus

#######
# API #
#######
def connectProbeInfo(pyCallable):
    infoSig = ChannelHandler.singleton.masterSignalsDict['probeInfo']
    infoSig.signal.connect(pyCallable)

class Central(QSplitter):

    " The main window. Emit tracker server events "

    def __init__(self, parent):
        super(Central, self).__init__(parent)
        self.setObjectName('monitorMain splitter')

        norrd.init(parent=self)
        #tko = TkorderMain.TkorderClient.singleton
        #tko.closeSignal.connect(self.saveLayoutState)
        Central.singleton   = self
        self.eventHandler       = ChannelHandler(self, 5)

        self.collapsed  = False

        #self.leftTree   = MonitorTreeArea.TreeContainer(self)
        #self.rightDash  = MonitorDashboardArea.DashboardStack(self)

        #self.addWidget(self.leftTree)
        #self.addWidget(self.rightDash)

        self.addWidget(QLabel('left', self))
        self.addWidget(QLabel('right', self))
        
        tko.addTopDockWidget(Summary(self), 'Monitori')
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
    
    def _restoreSettings(self):
        settings = QSettings("Noctopus NMS", "Monitor")
        self.restoreGeometry(settings.value("Monitor/geometry"))
        self.restoreState(settings.value("Monitor/state"))

    def closeEvent(self):
        settings = QSettings("Noctopus NMS", "monitor")
        settings.setValue("Monitor/geometry",   self.saveGeometry())
        settings.setValue("Monitor/state",      self.saveState())

class ChannelHandler(QObject):
    
    " This class handle other widgets subscription and emit message "
    " received by the server with Signal(). The method 'handleMSG' receive "
    " messages from the server "
    " She is also responsible of the channel group concept and max channel "
    " limitations."

    def __init__(self, parent, maxChans=3):
        super(ChannelHandler, self).__init__(parent)
        # simple init
        ChannelHandler.singleton = self

        #self.sc         = Supercast.Link.singleton
        #self.sc.setMessageProcessor('modTrackerPDU', self.handleMsg)
        #self.masterChan = 'target-MasterChan'
        
        # register handle probeInfo and targetInfo
        self.targets    = dict()
        self.probes     = dict()

        # channel handling
        self.subscribedChans    = list()
        self.pendingSubscribe   = list()
        self.chanProxy          = dict()

        # signals
        self.masterSignalsDict = dict()
        self.masterSignalsDict['probeInfo']     = SimpleSignal(self)
        self.masterSignalsDict['targetInfo']    = SimpleSignal(self)
        self.masterSignalsDict['probeModInfo']  = SimpleSignal(self)
        self.masterSignalsDict['probeDump']     = SimpleSignal(self)
        self.masterSignalsDict['probeReturn']   = SimpleSignal(self)
        self.masterSignalsDict['probeEventMsg'] = SimpleSignal(self)

        # connect myself
        self.masterSignalsDict['probeInfo'].signal.connect(self._handleProbeInfo)
        self.masterSignalsDict['targetInfo'].signal.connect(self._handleTargetInfo)
        self.masterSignalsDict['probeDump'].signal.connect(self._handleProbeDump)
        self.masterSignalsDict['probeReturn'].signal.connect(self._handleProbeReturn)
        self.masterSignalsDict['probeEventMsg'].signal.connect(self._handleEventMsg)
        # END

    def handleMsg(self, msg):
        if      msg['msgType'] == 'probeReturn':
            self.masterSignalsDict['probeReturn'].signal.emit(msg)

        elif    msg['msgType'] == 'probeEventMsg':
            self.masterSignalsDict['probeEventMsg'].signal.emit(msg)

        elif    msg['msgType'] == 'probeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'rrdProbeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'eventProbeDump':
            self.masterSignalsDict['probeDump'].signal.emit(msg)

        elif    msg['msgType'] == 'probeInfo':
            self.masterSignalsDict['probeInfo'].signal.emit(msg)

        elif    msg['msgType'] == 'targetInfo':
            self.masterSignalsDict['targetInfo'].signal.emit(msg)

        elif    msg['msgType'] == 'probeModInfo':
            self.masterSignalsDict['probeModInfo'].signal.emit(msg)

        elif    msg['msgType'] == 'authAck':
            self._autoSubscribe()

        elif    msg['msgType'] == 'subscribeOk':
            self._handleSubscribeOk(msg)

        elif    msg['msgType'] == 'unSubscribeOk':
            self._handleUnsubscribeOk(msg)


        else: 
            print "unknown msg received", msg['msgType']

    def subscribe(self, viewObject, channel):
        if channel in self.subscribedChans:
            self.chanProxy[channel].synchronizeView(viewObject)
            self.chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
        elif channel in self.pendingSubscribe:
            self.chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
        else:
            self.chanProxy[channel] = Channel(self, channel)
            self.chanProxy[channel].signal.connect(viewObject.handleProbeEvent)
            self._subscribe(channel)

    def unsubscribe(self, viewObject, channel):
        self.chanProxy[channel].signal.disconnect(viewObject.handleProbeEvent)

    def _subscribe(self, channel):
        self.pendingSubscribe.append(channel)
        self.sc.subscribe(channel)

    def _unsubscribe(self, channel):
        self.pendingUnsubscribe.append(channel)
        self.sc.unsubscribe(channel)

    def _handleSubscribeOk(self, msg):
        channel = msg['value']
        if channel == self.masterChan: return
        self.pendingSubscribe.remove(channel)
        self.subscribedChans.append(channel)

    def _handleUnsubscribeOk(self, msg):
        channel = msg['value']
        if channel == self.masterChan: return
        self.chanSignals[channel].destroy()
        del self.chanSignals[channel]

    def _handleProbeDump(self, msg):
        channel = msg['value']['id']
        self.chanProxy[channel].handleDump(msg)

    def _handleProbeReturn(self, msg):
        channel = msg['value']['id']
        self.chanProxy[channel].handleReturn(msg)

    def _handleEventMsg(self, msg):
        channel = msg['value']['id']
        self.chanProxy[channel].handleEvent(msg)

    def _autoSubscribe(self):
        self.sc.subscribe(self.masterChan)

    def _handleProbeInfo(self, msg):
        probeInfo   = msg['value']
        probeName   = probeInfo['name']
        self.probes[probeName] = probeInfo

    def _handleTargetInfo(self, msg):
        targetInfo  = msg['value']
        targetName  = targetInfo['name']
        self.targets[targetName] = targetInfo


class Channel(QObject):
    signal = Signal(dict)
    def __init__(self, parent, probeName):
        super(Channel, self).__init__(parent)
        self.probeDict = ChannelHandler.singleton.probes[probeName]
        self.name = probeName
        self.loggerTextState    = None
        self.loggerEventState   = None
        self.rrdFiles           = None

    def synchronizeView(self, view):
        if self.loggerTextState != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'btracker_logger_text'
            dumpMsg['data']     = self.loggerTextState
            view.handleProbeEvent(dumpMsg)
        if self.rrdFiles != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'btracker_logger_rrd'
            dumpMsg['data']     = self.rrdFiles
            view.handleProbeEvent(dumpMsg)
        if self.loggerEventState != None:
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = 'tracker_events'
            dumpMsg['data']     = self.loggerEventState
            view.handleProbeEvent(dumpMsg)
        
    def handleDump(self, msg):
        dumpType = msg['value']['logger']
        data     = msg['value']['data']
        if   dumpType == 'btracker_logger_text':
            self.loggerTextState = deque(data.split('\n'))
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = self.loggerTextState
            self.signal.emit(dumpMsg)
        elif dumpType == 'tracker_events':
            self.loggerEventState = msg['value']['data']
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = self.loggerEventState
            self.signal.emit(dumpMsg)
        elif dumpType == 'btracker_logger_rrd':
            self.rrdFiles = dict()
            for key in data:
                rrdFile = QTemporaryFile(self)
                rrdFile.open()
                rrdFile.write(str(data[key]))
                rrdFile.close()
                fileName = rrdFile.fileName()
                self.rrdFiles[key] = fileName 
            dumpMsg = dict()
            dumpMsg['msgType']  = 'probeDump'
            dumpMsg['logger']   = dumpType
            dumpMsg['data']     = self.rrdFiles
            self.signal.emit(dumpMsg)
            
            #self.rrdUpdateString = self.probeDict['loggers']['btracker_logger_rrd']['update']
            #self.rrdMacroBinds   = self.probeDict['loggers']['btracker_logger_rrd']['binds']
            #self.rrdFile = QTemporaryFile(self)
            #self.rrdFile.open()
            #self.rrdFile.write(data)
            #self.rrdFile.close()
            #self.rrdFileName = self.rrdFile.fileName()
            #dumpMsg = dict()
            #dumpMsg['msgType']  = 'probeDump'
            #dumpMsg['logger']   = dumpType
            #dumpMsg['data']     = self.rrdFileName

    def handleReturn(self, msg):
        if self.rrdFiles != None:
            self._updateRrdDb(msg)
        if self.loggerTextState != None:
            self._updateLoggerText(msg)
        self.signal.emit(msg)

    def handleEvent(self, msg):
        self.loggerEventState.append(msg['value']['data'])
        self.signal.emit(msg)

    def _updateLoggerText(self, msg):
        self.loggerTextState.append(msg['value']['originalRep'])
        if len(self.loggerTextState) > 50:
            self.loggerTextState.popleft()

    def _updateRrdDb(self, msg):
        rrdConf   = self.probeDict['loggers']['btracker_logger_rrd']
        rrdFiles  = self.rrdFiles
        keyVals   = msg['value']['keyVals']
        for rrd in rrdFiles.keys():
            updateString = rrdConf[rrd]['update']
            for bind in rrdConf[rrd]['binds']:
                macro   = rrdConf[rrd]['binds'][bind]
                try:
                    value = keyVals[bind]
                except KeyError:
                    print "missing bind. I will not update the rrd"
                    break
                updateString = updateString.replace(macro, str(value))

            template    = re.findall(r'--template\s+[^\s]+',  updateString)
            template    = re.sub(r'--template\s+', r'', template[0])
            rrdvalues   = re.findall(r'N:[^\s]+', updateString)
            rrdvalues   = rrdvalues[0]
            commandString = 'update %s --template %s %s' % (rrdFiles[rrd], template, rrdvalues)
            norrdQtThreaded.cmd(commandString)

class SimpleSignal(QObject):
    signal = Signal(dict)
    def __init__(self, parent):
        super(SimpleSignal, self).__init__(parent)

class AbstractChannelQFrame(QFrame):
    def __init__(self, parent, channel):
        super(AbstractChannelQFrame, self).__init__(parent)
        self.__channel = channel

    def connectProbe(self):
        ChannelHandler.singleton.subscribe(self, self.__channel)

    def handleProbeEvent(self, msg): 
        print self, ":you should handle this message: ", msg['msgType']

    def __disconnectProbe(self):
        ChannelHandler.singleton.unsubscribe(self, self.__channel)

    def destroy(self):
        self.__disconnectProbe()
        QFrame.destroy(self)
