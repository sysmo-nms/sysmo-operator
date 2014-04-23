from    PySide.QtCore       import Qt
from    PySide.QtGui        import (
    QTreeWidget,
    QTreeWidgetItem,
    QStyledItemDelegate,
    QStyleOptionProgressBar,
    QApplication,
    QStyle
)

from    noctopus_widgets    import NFrameContainer, NGridContainer
import  opus.monitor.api    as monapi

class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(PerfTree(self), 0,0)
        self.setLayout(self._grid)

class PerfTree(QTreeWidget):
    def __init__(self, parent):
        super(PerfTree, self).__init__(parent)
        self.setColumnCount(2)
        self.setHeaderLabels([self.tr('Elements'), self.tr('Performances')])
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)
        self.setItemDelegate(PerfDelegate(self))

    def dropEvent(self, event):
        stri  = monapi.getProbeSelection()
        items = []
        for i in range(len(stri)):
            it = QTreeWidgetItem(self)
            it.setText(0, stri[i])
            items.append(it)
        self.insertTopLevelItems(0, items)
        event.setDropAction(Qt.IgnoreAction)
        QTreeWidget.dropEvent(self, event)

class PerfDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(PerfDelegate, self).__init__(parent)

    def paint(self, painter, options, index):
        if index.column() == 1:
            probar          = QStyleOptionProgressBar()
            probar.rect     = options.rect
            probar.minimum  = 0
            probar.maximum  = 100
            probar.progress = 50
            st = QApplication.style()
            st.drawControl(QStyle.CE_ProgressBar, probar, painter)
            QStyledItemDelegate.paint(self, painter, options, index)
        else:
            QStyledItemDelegate.paint(self, painter, options, index)
        QStyledItemDelegate.paint(self, painter, options, index)
