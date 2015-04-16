from PyQt5.QtWidgets import QDialog, QMdiArea, QLabel
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

class DashboardView(QDialog):
    elements = dict()
    def __init__(self, target, parent=None):
        QDialog.__init__(self, parent)
        sysmapi.nConnectWillClose(self.close)
        mdi  = QMdiArea(self)
        ctrl = QLabel('controls', self)
        grid = NGrid(self)
        grid.addWidget(ctrl, 0,0)
        grid.addWidget(mdi,  1,0)

        for p in monapi.getProbesFor(target):
            mdi.addSubWindow(LoggerMDI(p['name']))

        self._mdi    = mdi
        self.show()
