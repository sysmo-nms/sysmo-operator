from PyQt5.QtWidgets import QDialog, QMdiArea
from monitor.windows.performances import LoggerMDI

from    sysmo_widgets    import (
    NFrameContainer,
    NGridContainer,
    NFrame,
    NGrid
)

import monitor.api as monapi

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
        mdi  = QMdiArea(self)
        grid = NGrid(self)
        grid.addWidget(mdi, 0,0)

        for p in monapi.getProbesFor(target):
            mdi.addSubWindow(LoggerMDI(p['name']))

        self._mdi    = mdi
        self.show()
