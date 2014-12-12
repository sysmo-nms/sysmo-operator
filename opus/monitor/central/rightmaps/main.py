from    PySide.QtCore   import Qt, QSize
from    PySide.QtGui   import (
    QFrame,
    QPushButton,
    QTabWidget,
    QTabBar,
    QMdiArea
)

from    opus.monitor.widgets         import OSMView
from    opus.monitor.central.rightmaps.dependencies import MDIDependencies
from    noctopus_widgets             import (
    NFrameContainer,
    NGridContainer,
    NGrid,
    NFrame
)

import  nocapi

class RightMapsContainer(NFrame):
    def __init__(self, parent):
        super(RightMapsContainer, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self._mapsControls = RightMapsControls(self)
        grid = NGrid(self)
        grid.addWidget(self._mapsControls,  0,0)
        grid.addWidget(RightMapsTabs(self), 1,0)
        grid.setRowStretch(0,0)
        grid.setRowStretch(1,1)
        grid.setVerticalSpacing(6)

class RightMapsControls(NFrameContainer):
    def __init__(self, parent):
        super(RightMapsControls, self).__init__(parent)
        grid = NGridContainer(self)

        toOsm = QPushButton(self)
        toOsm.setFixedWidth(30)
        toOsm.setContentsMargins(0,0,0,0)
        toOsm.setIcon(nocapi.nGetIcon('list-add'))
        grid.addWidget(toOsm, 0,0)

        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)

class RightMapsTabs(QTabWidget):
    def __init__(self, parent):
        super(RightMapsTabs, self).__init__(parent)
        tabBar = self.tabBar()
        tabBar.setUsesScrollButtons(True)
        tabBar.setExpanding(True)

        self.setTabPosition(QTabWidget.North)
        self.setElideMode(Qt.ElideRight)
        self.setMovable(True)

        self._osmc = OSMContainer(self)
        self._depc = DepContainer(self)
        osmicon = nocapi.nGetIcon('internet-web-browser')
        depicon = nocapi.nGetIcon('network-workgroup')
        self.addTab(self._depc,depicon,self.tr('Dependencies'))

        self.addTab(self._osmc,osmicon,self.tr('Map'))

class OSMContainer(NFrameContainer):
    def __init__(self, parent):
        super(OSMContainer, self).__init__(parent)
        grid = NGrid(self)
        self._osm = OSMView(self)
        grid.addWidget(self._osm, 0,0)

class DepContainer(NFrameContainer):
    def __init__(self, parent):
        super(DepContainer, self).__init__(parent)
        grid = NGrid(self)
        self._dependencies = MDIDependencies(self)
        grid.addWidget(self._dependencies, 0,0)
