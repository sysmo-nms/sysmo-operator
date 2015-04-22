from PyQt5.QtWidgets import QMdiArea,QLabel,QWidget,QAction,QMenu,QMenuBar
from PyQt5.QtCore import Qt
from monitor.windows.performances import LoggerMDI

from    sysmo_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid
)

import monitor.api as monapi
import sysmapi

def openDashboardFor(target):
    if target in list(DashboardView.elements.keys()):
        DashboardView.elements[target].show()
        return
    else:
        DashboardView.elements[target] = DashboardView(target)

class DashboardView(QWidget):
    elements = dict()
    def __init__(self, target, parent=None):
        super(DashboardView, self).__init__(parent)
        sysmapi.nConnectWillClose(self.close)
        mdi  = QMdiArea(self)
        fscreen = QAction('Full Screen', self)
        fscreen.triggered.connect(self._fscreen)
        viewMode = QAction('View Mode', self)
        viewMode.triggered.connect(self._toggleViewMode)
        cascade = QAction('Cascade layout', self)
        cascade.triggered.connect(mdi.cascadeSubWindows)
        tile    = QAction('Tile layout', self)
        tile.triggered.connect(mdi.tileSubWindows)
        save    = QAction('Save layout', self)
        restaure = QAction('Restaure layout', self)
        quit    = QAction('Quit', self)
        quit.triggered.connect(self.close)
        menu = QMenu('Dashboard', self)
        menu.addAction(fscreen)
        menu.addAction(viewMode)
        menu.addSeparator()
        menu.addAction(cascade)
        menu.addAction(tile)
        menu.addAction(save)
        menu.addAction(restaure)
        menu.addAction(quit)
        ctrl = QMenuBar(self)
        ctrl.addMenu(menu)
        grid = NGrid(self)
        grid.addWidget(ctrl, 0,0)
        grid.addWidget(mdi,  1,0)

        for p in monapi.getProbesFor(target):
            mdi.addSubWindow(LoggerMDI(p['name']))

        self._mdi    = mdi
        self.show()
        self._full = False

    def _fscreen(self):
        self.setWindowState(self.windowState() ^ Qt.WindowFullScreen)

    def _toggleViewMode(self):
        if self._mdi.viewMode() == QMdiArea.TabbedView:
            self._mdi.setViewMode(QMdiArea.SubWindowView)
        else:
            self._mdi.setViewMode(QMdiArea.TabbedView)
