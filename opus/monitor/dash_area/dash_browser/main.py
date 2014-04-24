from    PySide.QtGui        import (
    QTreeWidget,
    QTreeWidgetItem
)
from    PySide.QtCore       import Qt
from    noctopus_widgets    import NFrameContainer, NGridContainer
from    opus.monitor.widgets    import TextLog
import  opus.monitor.api    as monapi

class BrowserDash(NFrameContainer):
    def __init__(self, parent):
        super(BrowserDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(BrowserTree(self), 0,0)
        self.setLayout(self._grid)

class BrowserTree(QTreeWidget):
    def __init__(self, parent):
        super(BrowserTree, self).__init__(parent)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr('Elements'), self.tr('Text logs')])
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)

    def dropEvent(self, event):
        stri  = monapi.getProbeSelection()
        for i in range(len(stri)):
            it = QTreeWidgetItem(self)
            it.setText(0, stri[i])
            self.insertTopLevelItem(0, it)
            self.setItemWidget(it, 1, TextLog(self, stri[i]))
        event.setDropAction(Qt.IgnoreAction)
        QTreeWidget.dropEvent(self, event)
