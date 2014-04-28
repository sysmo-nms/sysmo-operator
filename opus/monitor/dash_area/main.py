from    PySide.QtGui        import (
    QTabWidget,
    QMdiArea,
    QFrame,
    QPushButton
)
from    PySide.QtCore       import Qt
from    noctopus_widgets    import (
    NFrame,
    NGrid
)
from    opus.monitor.dash_area.drop_manager import DropModel
from    opus.monitor.dash_area.controls import DashActions
from    opus.monitor.dash_area.dash     import Dashboard
from    noctopus_infobutton             import NInfoButton
import  nocapi

class DashContainer(NFrame):
    def __init__(self, parent):
        super(DashContainer, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setContentsMargins(6,4,2,4)
        self._dropMan   = DropModel(self)
        self._controls  = DashActions(self)
        self._tabs      = DashTab(self)

        self._grid      = NGrid(self)
        self._grid.setVerticalSpacing(6)
        self._grid.addWidget(self._controls,    0,0)
        self._grid.addWidget(self._tabs,        1,0)
        self._grid.setRowStretch(0,0)
        self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        tabBar = self.tabBar()
        tabBar.setUsesScrollButtons(True)
        tabBar.setExpanding(True)
        helpButton = NInfoButton(self)
        addButton = QPushButton(self)
        addButton.setIcon(nocapi.nGetIcon('list-add'))
        addButton.setFlat(True)
        addButton.setToolTip(self.tr('Create a new tab'))
        self.setElideMode(Qt.ElideRight)
        self.setMovable(True)
        self.setCornerWidget(addButton,  corner=Qt.TopLeftCorner)
        self.setCornerWidget(helpButton, corner=Qt.TopRightCorner)
        self.addTab(
            Dashboard(self),
            nocapi.nGetIcon('applications-development'),
            self.tr('Default')
        )
