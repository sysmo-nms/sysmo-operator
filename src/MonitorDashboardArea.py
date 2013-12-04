from    PySide.QtGui        import *
from    PySide.QtCore       import *
from    MonitorProxyEvents  import ChannelHandler
from    MonitorViewMDI      import MDIView
from    MonitorViewWorking  import WorkView
from    copy                import copy
import  TkorderIcons

class Dashboard(QFrame):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        Dashboard.singleton = self
        self.chanHandler = ChannelHandler.singleton
        self.dash       = DashTab(self)
        self.control    = DashControls(self)
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

        grid = QGridLayout(self)
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(toolbar,     0,0)
        grid.addWidget(verticalBar, 0,1)
        grid.addWidget(ViewControls(self), 0,2)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,0)
        grid.setColumnStretch(2,1)

        self.setLayout(grid)

class ViewControls(QFrame):
    def __init__(self, parent):
        super(ViewControls, self).__init__(parent)
        start = QLabel('start:', self)
        startSlide = QSlider(self)
        startSlide.setOrientation(Qt.Horizontal)
        stop  = QLabel('stop:', self)
        stopSlide = QSlider(self)
        stopSlide.setOrientation(Qt.Horizontal)

        grid = QGridLayout(self)
        grid.addWidget(start,       0,0)
        grid.addWidget(startSlide,   0,1)
        grid.addWidget(stop,        0,2)
        grid.addWidget(stopSlide,    0,3)
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,0)
        grid.setColumnStretch(3,1)
        self.setLayout(grid)


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
        self.addTab(mdiView,  'Dashboard')
