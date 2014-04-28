from    PySide.QtCore       import Qt
from    PySide.QtGui        import (
    QTreeWidget
)

from    noctopus_widgets    import (
    NFrameContainer,
    NGridContainer
)

#from    opus.monitor.dash_area.dash_perfs.rrds  import RrdArea, RrdAreaTest
from    opus.monitor.dash_area.drop_manager import DropMan
import  opus.monitor.api                    as monapi
from    opus.monitor.widgets                import TextLog


class PerfDash(NFrameContainer):
    def __init__(self, parent):
        super(PerfDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(PerfTree(self), 0,0)
        self.setLayout(self._grid)

class PerfTree(QTreeWidget):
    def __init__(self, parent):
        super(PerfTree, self).__init__(parent)
        self._dropMan = DropMan.singleton
        self.setSortingEnabled(False)
        self.setAcceptDrops(True)
        self.setHeaderHidden(True)


    def dropEvent(self, event):
        self._model.handleDropEvent(event)
        event.setDropAction(Qt.IgnoreAction)
        QTreeView.dropEvent(self, event)

#     def dropEvent(self, event):
#         stri  = monapi.getProbeSelection()
#         for i in range(len(stri)):
#             it = QTreeWidgetItem(self)
#             it.setText(0, stri[i])
#             self.insertTopLevelItem(0, it)
#             self.setItemWidget(it, 1, TextLog(self, stri[i]))
#         event.setDropAction(Qt.IgnoreAction)
#         QTreeWidget.dropEvent(self, event)

# class PerfItem(QStyledItemDelegate):
#     def __init__(self, parent):
#         super(PerfItem, self).__init__(parent)
# 
#     def paint(self, painter, options, index):
#         if index.column() == 1:
#             probar          = QStyleOptionProgressBar()
#             probar.rect     = options.rect
#             probar.minimum  = 0
#             probar.maximum  = 100
#             probar.progress = 50
#             st = QApplication.style()
#             st.drawControl(QStyle.CE_ProgressBar, probar, painter)
#         else:
#             QStyledItemDelegate.paint(self, painter, options, index)
