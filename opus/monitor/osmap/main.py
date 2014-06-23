from    PySide.QtGui   import (
    QFrame
)

from    opus.monitor.widgets         import OSMView
from    noctopus_widgets             import (
    NFrameContainer,
    NGridContainer,
    NGrid,
    NFrame
)

import  nocapi

class OSMapContainer(NFrame):
    def __init__(self, parent):
        super(OSMapContainer, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        grid = NGrid(self)
        grid.addWidget(OSMView(self), 0,0)
        self.setLayout(grid)
