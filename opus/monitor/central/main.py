from PySide.QtGui import QSplitter
from PySide.QtCore import QSettings, QTimeLine
from    noctopus_widgets    import (
    NFrameContainer, NFrame,
    NGridContainer, NGrid
)

from    opus.monitor.central.tree.main          import ProbesTree
from    opus.monitor.central.timeline.main      import Timeline
from    opus.monitor.central.osmap.main         import OSMapContainer
#import  opus.monitor.api as monapi
import  nocapi

class TreeContainer(NFrameContainer):
    def __init__(self, parent):
        super(TreeContainer, self).__init__(parent)
        TreeContainer.singleton = self
        self._treeStack  = TreeStack(self)
        self._timeline   = Timeline(self)
        self._grid = NGridContainer(self)
        self._grid.setVerticalSpacing(6)

        self._grid.addWidget(self._treeStack,          1, 0)
        self._grid.addWidget(self._timeline,           2, 0)

        self._grid.setRowStretch(1,1)
        self._grid.setRowStretch(2,0)
        self.setLayout(self._grid)

class TreeStack(QSplitter):
    def __init__(self, parent):
        super(TreeStack, self).__init__(parent)
        self._timeline = QTimeLine(100, self)
        self._timeline.setUpdateInterval(20)
        self._timeline.frameChanged[int].connect(self._resize)
        nocapi.nConnectAppToggled(self._toggleSplitter)
        nocapi.nConnectWillClose(self._saveSettings)
        self._osmap = OSMapContainer(self)
        self._ptree = ProbesTree(self)
        self.addWidget(self._ptree)
        self.addWidget(self._osmap)
        self._loadSettings()

    def _saveSettings(self):
        state = self.saveState()
        visible = self._osmap.isVisible()
        settings = QSettings()
        settings.setValue('monitor/tree_stack', state)
        settings.setValue('monitor/tree_stack_visible', visible)

    def _loadSettings(self):
        settings = QSettings()
        state    = settings.value('monitor/tree_stack')
        visible  = settings.value('monitor/tree_stack_visible')
        if state != None:
            self.restoreState(state)

        if visible != None:
            if visible == 'false':
                self._osmap.hide()
        
    def _toggleSplitter(self, msg):
        if msg['id']        != 'monitor': return
        if msg['button']    != 'left': return
        if self._osmap.isVisible() == True:
            width = self._osmap.width()
            self._tstop = 0
            self._timeline.setFrameRange(width, 0)
            self._timeline.start()
        else:
            width = 400
            self._tstop = 400
            self._timeline.setFrameRange(0, width)
            self._timeline.start()
            self._osmap.show()

    def _resize(self, size):
        print "resize: ", size
        self._osmap.setFixedWidth(size)
        if self._tstop == size:
            if self._tstop == 0:
                self._osmap.hide()
            
