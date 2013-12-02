from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorProxyEvents  import ChannelHandler
from    MonitorViewMDI      import MDIView
from    MonitorViewWorking  import WorkView
from    copy                import copy

class Dashboard(QFrame):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        Dashboard.singleton = self
        self.chanHandler = ChannelHandler.singleton
        self.dash   = DashTab(self)
        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.dash,           0,0)
        self.setLayout(grid)
        self.selection = set([])

    def userNewSelection(self, chanSelection):
        targetSelection = set([])
        probeSelection   = set([])

        # filter targets and probes
        for chan in chanSelection:
            if chan in self.chanHandler.targets.keys():
                targetSelection.add(chan)
            else:
                probeSelection.add(chan)

        # extract probes with target as parent
        for target in targetSelection:
            for probe in self.chanHandler.probes.keys():
                if self.chanHandler.probes[probe]['target'] == target:
                    probeSelection.add(probe)

        # remove unselected and allready handled probes
        iterate = copy(self.selection)
        for probe in iterate:
            if probe not in probeSelection:
                self.destroyProbeView(probe)
            else:
                probeSelection.remove(probe)

        # finaly probeSelection only contain non handled probes, and
        # self.selection have removed unselected probeViews.
        for probe in probeSelection:
            self.createProbeView(probe)

    def destroyProbeView(self, probe):
        self.selection.remove(probe)
        for view in self.dash.views:
            view.destroyProbe(probe)

    def createProbeView(self, probe):
        self.selection.add(probe)
        for view in self.dash.views:
            view.createProbe(probe)

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        self.stackDict  = dict()
        self.views      = list()
        workView    = WorkView(self)
        mdiView     = MDIView(self)
        self.views.append(workView)
        self.views.append(mdiView)
        self.addTab(workView, 'Work view')
        self.addTab(mdiView,  'MDI view')
