from PySide.QtGui import (
    QLabel,
    QPushButton,
    QButtonGroup,
    QStackedLayout
)
from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer,
    NGrid
)
import nocapi


from opus.monitor.dash_area.dash_mdi.main       import MdiDash
from opus.monitor.dash_area.dash_browser.main   import BrowserDash
from opus.monitor.dash_area.dash_wmap.main      import WmapDash
from opus.monitor.dash_area.dash_graphic.main   import GraphicDash
from opus.monitor.dash_area.dash_timeline.main  import TimelineDash
from opus.monitor.dash_area.dash_perfs.main     import PerfDash

class Dashboard(NFrameContainer):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        self._controls  = DashboardControls(self)
        self._stack     = DashboardStack(self)
        self._controls.buttonGroup.buttonClicked[int].connect(self._stack.setCurrentIndex)
        self._grid = NGrid(self)
        self._grid.addWidget(self._controls,  0,0)
        self._grid.addWidget(self._stack,     1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

class DashboardControls(NFrameContainer):
    def __init__(self, parent):
        super(DashboardControls, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.setHorizontalSpacing(4)
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)


        browse  = QPushButton(self.tr('browse'), self)
        browse.setCheckable(True)
        mdi     = QPushButton(self.tr('mdi'),    self)
        mdi.setCheckable(True)
        graphic = QPushButton(self.tr('graphic'),self)
        graphic.setCheckable(True)
        wmap    = QPushButton(self.tr('wmap'),   self)
        wmap.setCheckable(True)
        timeline = QPushButton(self.tr('timeline'),   self)
        timeline.setCheckable(True)
        perfs   = QPushButton(self.tr('perfs'),   self)
        perfs.setCheckable(True)

        self.buttonGroup.addButton(browse,    0)
        self.buttonGroup.addButton(mdi,       1)
        self.buttonGroup.addButton(graphic,   2)
        self.buttonGroup.addButton(wmap,      3)
        self.buttonGroup.addButton(timeline,  4)
        self.buttonGroup.addButton(perfs,     5)
        browse.setChecked(True)

        self._grid.addWidget(browse,      0,0)
        self._grid.addWidget(mdi,         0,1)
        self._grid.addWidget(graphic,     0,2)
        self._grid.addWidget(wmap,        0,3)
        self._grid.addWidget(timeline,    0,4)
        self._grid.addWidget(perfs,       0,5)

        self._grid.setColumnStretch(0,0)
        self._grid.setColumnStretch(1,0)
        self._grid.setColumnStretch(9,1)
        self.setLayout(self._grid)

class DashboardStack(NFrameContainer):
    def __init__(self, parent):
        super(DashboardStack, self).__init__(parent)
        self._stackLayout = QStackedLayout(self)

        self._browser       = BrowserDash(self)
        self._mdi           = MdiDash(self)
        self._graphic       = GraphicDash(self)
        self._wmap          = WmapDash(self)
        self._timeline      = TimelineDash(self)
        self._perfs         = PerfDash(self)
        self._stackLayout.insertWidget(0, self._browser)
        self._stackLayout.insertWidget(1, self._mdi)
        self._stackLayout.insertWidget(2, self._graphic)
        self._stackLayout.insertWidget(3, self._wmap)
        self._stackLayout.insertWidget(4, self._timeline)
        self._stackLayout.insertWidget(5, self._perfs)
        self.setLayout(self._stackLayout)

    def setCurrentIndex(self, index):
        self._stackLayout.setCurrentIndex(index)
