from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorProxyEvents  import ChannelHandler
from    MonitorViewMDI      import MDIView
from    MonitorViewWorking  import WorkView
from    PerformanceViews    import *
from    CommonWidgets       import *
from    copy                import copy
import  TkorderIcons

class DashboardStack(QFrame):
    def __init__(self, parent):
        super(DashboardStack, self).__init__(parent)
        DashboardStack.singleton = self
        self.stack = QStackedLayout(self)
        self.expertDashboard = Dashboard(self)
        self.simpleDashboard = DashboardSimplified(self)
        self.stack.addWidget(self.simpleDashboard)
        self.stack.addWidget(self.expertDashboard)
        self.stack.setCurrentWidget(self.expertDashboard)
        self.setLayout(self.stack)

    def setSimpleView(self):
        self.stack.setCurrentWidget(self.simpleDashboard)

    def setExpertView(self):
        self.stack.setCurrentWidget(self.expertDashboard)

class DashboardSimplified(QFrame):
    def __init__(self, parent):
        super(DashboardSimplified, self).__init__(parent)
        sig = ChannelHandler.singleton.masterSignalsDict['probeInfo']
        sig.signal.connect(self.handleProbeInfo)
        grid = QGridLayout(self)
        grid.setVerticalSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        self.dash = MDIView(self)
        self.dash.setFrameShape(QFrame.StyledPanel)
        self.dash.setFrameShadow(QFrame.Raised)
        grid.addWidget(self.dash, 1,0)
        self.setLayout(grid)

    def handleProbeInfo(self, msg):
        name = msg['value']['name']
        self.dash.createProbeView(name)

class Dashboard(QFrame):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        Dashboard.singleton = self
        self.chanHandler = ChannelHandler.singleton
        self.dash       = DashTab(self)
        self.control    = DashControls(self)

        self.timelineSlide = self.control.viewControls.timelineSlide
        self.stopSlide     = self.control.viewControls.stopSlide

        grid            = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.control, 0,0)
        grid.addWidget(self.dash,   1,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        self.setLayout(grid)
        self.selection = set([])

    def userNewSelection(self, chanSelection):
        targetSelection     = set([])
        probeSelection      = set([])

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
            view.deleteProbeView(probe)

    def createProbeView(self, probe):
        self.selection.add(probe)
        for view in self.dash.views:
            view.createProbeView(probe)

class DashControls(QFrame):
    def __init__(self, parent):
        super(DashControls, self).__init__(parent)
        searchLine  = QLineEdit(self)
        searchLine.setPlaceholderText('Filter')
        toolbar = QToolBar(self)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.setFixedWidth(351)
        toolbar.addAction(TkorderIcons.get('edit-clear'), 'Clear')
        toolbar.addAction(TkorderIcons.get('document-save-as'), 'Save')
        toolbar.addAction(TkorderIcons.get('go-first'), 'go first')
        toolbar.addAction(TkorderIcons.get('go-previous'), 'go previous')
        toolbar.addAction(TkorderIcons.get('go-next'), 'go next')
        toolbar.addAction(TkorderIcons.get('go-last'), 'go last')
        toolbar.addWidget(searchLine)

        verticalBar = QFrame(self)
        verticalBar.setFrameShape(QFrame.VLine)
        verticalBar.setFrameShadow(QFrame.Sunken)



        #self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(35)

        self.viewControls = ViewControls(self)
        grid = QGridLayout(self)
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(toolbar,     0,0)
        grid.addWidget(verticalBar, 0,1)
        grid.addWidget(self.viewControls, 0,2)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)

        self.setLayout(grid)

class ViewControls(QFrame):
    def __init__(self, parent):
        super(ViewControls, self).__init__(parent)
        timeline = QLabel('Timeline:', self)
        self.timelineSlide = QSlider(self)
        self.timelineSlide.setMinimum(30)
        self.timelineSlide.setMaximum(604800)
        self.timelineSlide.setValue(3600)
        self.timelineInfo = QLabel(self)
        self.timelineInfo.setText('hell')
        self.timelineSlide.valueChanged.connect(self.updateTimelineLabel)

        self.timelineSlide.setOrientation(Qt.Horizontal)

        stop  = QLabel('stop:', self)
        self.stopSlide = QSlider(self)
        self.stopSlide.setOrientation(Qt.Horizontal)
        self.stopSlide.setMinimum(-604800)
        self.stopSlide.setMaximum(0)
        self.stopSlide.setValue(0)
        self.stopInfo = QLabel(self)
        self.stopInfo.setText('hell')
        self.stopSlide.valueChanged.connect(self.updateStopLabel)

        grid = QGridLayout(self)
        grid.addWidget(timeline,        0,0)
        grid.addWidget(self.timelineSlide,   0,1)
        grid.addWidget(self.timelineInfo,    0,2)
        grid.addWidget(stop,            0,3)
        grid.addWidget(self.stopSlide,       0,4)
        grid.addWidget(self.stopInfo,        0,5)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,0)
        grid.setColumnStretch(4,1)
        grid.setColumnStretch(5,0)
        self.setLayout(grid)

    def updateTimelineLabel(self, value):
        self.timelineInfo.setText(str(value))

    def updateStopLabel(self, value):
        self.stopInfo.setText(str(value))

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        self.stackDict  = dict()
        self.views      = list()
        workView        = WorkView(self)
        mdiView         = MDIView(self)
        perfView        = PerformanceMap(self)

        self.views.append(mdiView)
        self.views.append(workView)

        self.insertTab(0, mdiView,  'Dashboard')
        self.insertTab(1, workView, 'Explorer')
        self.insertTab(2, perfView, 'Performance map')
        self.setCurrentWidget(mdiView)
        self.setTabEnabled(2,False)
