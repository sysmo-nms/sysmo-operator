from    PySide.QtGui    import *
from    PySide.QtCore   import *

import  nocapi
from    opus.monitor                 import norrd
from    opus.monitor.trees_area.main import TreeContainer
from    opus.monitor.dash_area.main  import DashContainer
from    opus.monitor.channel_proxy   import ChanHandler
from    noctopus_widgets             import NSplitterContainer

#from    opus.monitor.widgets       import *

class Central(NSplitterContainer):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        Central.singleton = self
        nocapi.nConnectWillClose(self._willClose)
        self._initRrdtool()
        self._initChanProxy()
        self._initLayout()
        self._initDockWidget()
        self._initToggle()
        self._initViewMode()
        self._readSettings()

    def _initViewMode(self):
        nocapi.nConnectViewMode(self.setViewMode)
        self.setViewMode(nocapi.nGetViewMode())

    def _initToggle(self):
        self._collapsed  = False
        nocapi.nConnectAppToggled(self.toggleButtonClicked)

    def _initDockWidget(self): pass
#         tko.addTopDockWidget(Summary(self), 'Monitori')

    def _initLayout(self):
#         self._rightDash  = MonitorDashboardArea.DashboardStack(self)
        self._leftTree  = TreeContainer(self)
        self._rightDash = DashContainer(self)
        self.addWidget(self._leftTree)
        self.addWidget(self._rightDash)

    def _initRrdtool(self):
        self._rrdtool = norrd.init(parent=self)

    def _initChanProxy(self): 
        self._eventHandler = ChanHandler(self, 5)

    def _readSettings(self):
        settings = QSettings("Noctopus NMS", "monitor")
        self.restoreGeometry(settings.value("monitor/geometry"))
        self.restoreState(settings.value("monitor/state"))

    def _willClose(self):
        settings = QSettings("Noctopus NMS", "monitor")
        settings.setValue("monitor/geometry",   self.saveGeometry())
        settings.setValue("monitor/state",      self.saveState())
        # close rrdtool thread (self._rrdtool.quit())

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
