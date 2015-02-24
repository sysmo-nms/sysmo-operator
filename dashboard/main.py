from    PyQt5.QtWidgets        import (
    QTabWidget,
    QMdiArea,
    QFrame,
    QPushButton,
    QMenu
)
from    PyQt5.QtCore       import Qt
from    PyQt5.QtGui        import QIcon
from    sysmo_widgets    import (
    NFrame,
    NGridContainer
)
from    dashboard.controls     import DashActions
from    dashboard.dash         import Dashboard
from    sysmo_infobutton                 import NInfoButton
import  sysmapi

class Central(NFrame):
    def __init__(self, parent):
        super(Central, self).__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        menu = QMenu('dashboard',self)
        menu.setIcon(QIcon(sysmapi.nGetPixmap('preferences-system-session')))
        #self._controls  = DashActions(self)
        self._tabs      = DashTab(self)

        self._grid      = NGridContainer(self)
        #self._grid.setVerticalSpacing(6)
        #self._grid.addWidget(self._controls,    0,0)
        self._grid.addWidget(self._tabs,        1,0)
        #self._grid.setRowStretch(0,0)
        #self._grid.setRowStretch(1,1)
        self.setLayout(self._grid)

class DashTab(QTabWidget):
    def __init__(self, parent):
        super(DashTab, self).__init__(parent)
        tabBar = self.tabBar()
        tabBar.setUsesScrollButtons(True)
        tabBar.setExpanding(True)
        helpButton = NInfoButton(self)
        addButton = QPushButton(self)
        addButton.setIcon(QIcon(sysmapi.nGetPixmap('list-add')))
        addButton.setFlat(True)
        addButton.setToolTip(self.tr('Create a new tab'))
        self.setElideMode(Qt.ElideRight)
        self.setMovable(True)
        self.setCornerWidget(addButton,  corner=Qt.TopLeftCorner)
        self.setCornerWidget(helpButton, corner=Qt.TopRightCorner)
        self.addTab(
            Dashboard(self),
            QIcon(sysmapi.nGetPixmap('applications-development')),
            self.tr('Default')
        )
