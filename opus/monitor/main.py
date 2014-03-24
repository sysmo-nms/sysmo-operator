from    PySide.QtGui    import *
from    PySide.QtCore   import *

import  noctopus_api
from    noctopus_widgets    import NSplitterContainer
#from    opus.monitor.widgets       import *
from    opus.monitor    import norrd

#from    MonitorProxyEvents  import ChannelHandler

#import  MonitorDashboardArea
#import  MonitorTreeArea
#import  TkorderMain

class Central(NSplitterContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        Central.singleton = self
        noctopus_api.nConnectWillClose(self._willClose)
        self._initRrdtool()
        self._initProxy()
        self._initLayout()
        self._initDockWidget()
        self._initToggle()
        self._initViewMode()
        self._readSettings()

    def _initViewMode(self):
        noctopus_api.nConnectViewMode(self.setViewMode)
        self.setViewMode(noctopus_api.nGetViewMode())

    def _initToggle(self):
        self._collapsed  = False
        noctopus_api.nConnectAppToggled(self.toggleButtonClicked)

    def _initDockWidget(self): pass
#         tko.addTopDockWidget(Summary(self), 'Monitori')

    def _initLayout(self):
#         self._leftTree   = MonitorTreeArea.TreeContainer(self)
#         self._rightDash  = MonitorDashboardArea.DashboardStack(self)
        self._leftTree = QLabel('left', self)
        self._rightDash = QLabel('right', self)
        self.addWidget(self._leftTree)
        self.addWidget(self._rightDash)

    def _initRrdtool(self):
        self._rrdtool = norrd.init(parent=self)

    def _initProxy(self): pass
        #self.eventHandler       = ChannelHandler(self, 5)

    def _readSettings(self):
        settings = QSettings("Noctopus NMS", "monitor")
        self.restoreGeometry(settings.value("monitor/geometry"))
        self.restoreState(settings.value("monitor/state"))

    def _willClose(self):
        settings = QSettings("Noctopus NMS", "monitor")
        settings.setValue("monitor/geometry",   self.saveGeometry())
        settings.setValue("monitor/state",      self.saveState())



#         self.targets    = dict()
#         self.initHexaPalettes()

    # CALLS from noctopus_* modules
    def toggleButtonClicked(self, app):
        if app != 'monitor': return
        if self._collapsed == False:
            self._leftTree.hide()
            self._collapsed = True
        elif self._collapsed == True:
            self._leftTree.show()
            self._collapsed = False

    def setViewMode(self, mode):
        print "set viewwwwwwwww mode ", mode


#     def initHexaPalettes(self):
# 
#         " For widgets who need hexadecimal version of the colors actualy used "
#         " by the application (rrdtool)"
# 
#         self.rgbDict    = dict()
#         self.rgbaDict   = dict()
#         pal             = self.palette()
#         constDict = {
#             'Window':       QPalette.Window,
#             'WindowText':   QPalette.WindowText,
#             'Base':         QPalette.Base,
#             'AlternateBase':    QPalette.AlternateBase,
#             'ToolTipBase':  QPalette.ToolTipBase,
#             'ToolTipText':  QPalette.ToolTipText,
#             'Text':         QPalette.Text,
#             'Button':       QPalette.Button,
#             'ButtonText':   QPalette.ButtonText,
#             'BrightText':   QPalette.BrightText,
#             'Light':        QPalette.Light,
#             'MidLight':     QPalette.Midlight,
#             'Dark':         QPalette.Dark,
#             'Mid':          QPalette.Mid,
#             'Shadow':       QPalette.Shadow
#         }
# 
#         for key in constDict.keys():
#             col         = pal.color(constDict[key])
#             (r,g,b,a)   = col.getRgb()
#             self.rgbaDict[key]  = "#%0.2X%0.2X%0.2X%0.2X" % (r,g,b,a)
#             self.rgbDict[key] = "#%0.2X%0.2X%0.2X" % (r,g,b)
#     
