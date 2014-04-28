from    PySide.QtGui        import (
    #QTreeWidget,
    #QTreeWidgetItem
    QTreeView,
    QStyledItemDelegate,
    QStyleOptionProgressBar,
    QApplication,
    QStyle,
    QLabel
)
from    PySide.QtCore       import Qt, QSize
from    noctopus_widgets    import NFrameContainer, NGridContainer
from    opus.monitor.dash_area.drop_manager import DropModel
from    opus.monitor.widgets    import TextLog
import  opus.monitor.api    as monapi

class BrowserDash(NFrameContainer):
    def __init__(self, parent):
        super(BrowserDash, self).__init__(parent)
        self._grid = NGridContainer(self)
        self._grid.addWidget(BrowserTree(self), 0,0)
        self.setLayout(self._grid)

class BrowserTree(QTreeView):
    def __init__(self, parent):
        super(BrowserTree, self).__init__(parent)
        self._model = DropModel.singleton
        self.setModel(self._model)
        self.setAcceptDrops(True)
        self.setItemDelegate(BrowserItem(self))
        self.setHeaderHidden(True)

    def dropEvent(self, event):
        self._model.handleDropEvent(event)
        event.setDropAction(Qt.IgnoreAction)
        QTreeView.dropEvent(self, event)

class BrowserItem(QStyledItemDelegate):
    def __init__(self, parent):
        super(BrowserItem, self).__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == 1:
            r = option.rect
            lab = QLabel("hello")
            lab.render(painter, r.topLeft())
            #painter.restore()
#             progress = 50
#             popt        = QStyleOptionProgressBar()
#             popt.rect   = option.rect
#             popt.minimum    = 0
#             popt.maximum    = 100
#             popt.progress   = progress
#             popt.text       = "joj"
#             popt.textVisible = True
#             QApplication.style().drawControl(QStyle.CE_ProgressBar, popt, painter)

        elif index.column() == 2:
            QStyledItemDelegate.paint(self, painter, option, index)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        if index.column() == 1:
            return QSize(100, 100)
        else:
            return QSize()

# class BrowserTree(QTreeWidget):
#     def __init__(self, parent):
#         super(BrowserTree, self).__init__(parent)
# 
#         self.setColumnCount(2)
#         self.setHeaderLabels([self.tr('Elements'), self.tr('Text logs')])
#         self.setSortingEnabled(False)
#         self.setAcceptDrops(True)
# 
#     def dropEvent(self, event):
#         stri  = monapi.getProbeSelection()
#         for i in range(len(stri)):
#             it = QTreeWidgetItem(self)
#             it.setText(0, stri[i])
#             self.insertTopLevelItem(0, it)
#             self.setItemWidget(it, 1, TextLog(self, stri[i]))
#         event.setDropAction(Qt.IgnoreAction)
#         QTreeWidget.dropEvent(self, event)
