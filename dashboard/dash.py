from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QLabel,
    QFrame,
    QPushButton,
    QButtonGroup,
    QStackedLayout
)
from    sysmo_widgets    import (
    NFrameContainer,
    NGridContainer,
    NGrid
)
import sysmapi


from dashboard.dash_mdi.main       import MdiDash
from dashboard.dash_wmap.main      import WmapDash
from dashboard.dash_graphic.main   import GraphicDash
from dashboard.dash_timeline.main  import TimelineDash

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

        " edit buttons "
        saveButton = QPushButton(self)
        saveButton.setToolTip(self.tr('Save modifications'))
        saveButton.setIcon(QIcon(sysmapi.nGetPixmap('document-save-as')))
        backButton = QPushButton(self)
        backButton.setToolTip(self.tr('Restore last saved state'))
        backButton.setIcon(QIcon(sysmapi.nGetPixmap('edit-undo')))
        separator = QFrame(self)
        separator.setFixedWidth(6)
        separator.setFrameShape(QFrame.NoFrame)
        separator.setFrameShadow(QFrame.Plain)

        

        " dash switcher button group"
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)


        mdi = QPushButton(self)
        mdi.setToolTip(self.tr('mdi'))
        mdi.setIcon(QIcon(sysmapi.nGetPixmap('preferences-system-windows')))
        mdi.setCheckable(True)

        graphic = QPushButton(self)
        graphic.setToolTip(self.tr('graphic'))
        graphic.setIcon(QIcon(sysmapi.nGetPixmap('x-office-drawing')))
        graphic.setCheckable(True)

        wmap = QPushButton(self)
        wmap.setToolTip(self.tr('wmap'))
        wmap.setIcon(QIcon(sysmapi.nGetPixmap('internet-web-browser')))
        wmap.setCheckable(True)

        timeline = QPushButton(self)
        timeline.setToolTip(self.tr('timeline'))
        timeline.setIcon(QIcon(sysmapi.nGetPixmap('appointment-new')))
        timeline.setCheckable(True)

        self.buttonGroup.addButton(mdi,       0)
        self.buttonGroup.addButton(graphic,   1)
        self.buttonGroup.addButton(wmap,      2)
        self.buttonGroup.addButton(timeline,  3)
        mdi.setChecked(True)

        " grid "
        self._grid.addWidget(saveButton,  0,0)
        self._grid.addWidget(backButton,  0,1)
        self._grid.addWidget(separator,   0,2)
        self._grid.addWidget(mdi,         0,3)
        self._grid.addWidget(graphic,     0,4)
        self._grid.addWidget(wmap,        0,5)
        self._grid.addWidget(timeline,    0,6)

        self._grid.setColumnStretch(0,0)
        self._grid.setColumnStretch(1,0)
        self._grid.setColumnStretch(2,0)
        self._grid.setColumnStretch(3,0)
        self._grid.setColumnStretch(4,0)
        self._grid.setColumnStretch(5,0)
        self._grid.setColumnStretch(6,0)
        self._grid.setColumnStretch(7,0)
        self._grid.setColumnStretch(8,0)
        self._grid.setColumnStretch(9,1)

        self.setLayout(self._grid)

class DashboardStack(NFrameContainer):
    def __init__(self, parent):
        super(DashboardStack, self).__init__(parent)
        self._stackLayout = QStackedLayout(self)

        self._mdi           = MdiDash(self)
        self._graphic       = GraphicDash(self)
        self._wmap          = WmapDash(self)
        self._timeline      = TimelineDash(self)
        self._stackLayout.insertWidget(0, self._mdi)
        self._stackLayout.insertWidget(1, self._graphic)
        self._stackLayout.insertWidget(2, self._wmap)
        self._stackLayout.insertWidget(3, self._timeline)
        self.setLayout(self._stackLayout)

    def setCurrentIndex(self, index):
        self._stackLayout.setCurrentIndex(index)
